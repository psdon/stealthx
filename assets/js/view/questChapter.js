import invokeParticleWithSB from './particlesWithSidebar.js'
import { addEventByElementId } from '../script';
import invokeEditorJS from '../module/editor.js'

export default function createQuest() {
    invokeParticleWithSB();
    addEventByElementId('upload_video_btn', 'click', (e) => {
        document.getElementById('video_hidden').click();
    })

    addEventByElementId('video_hidden', 'change', (e) => {
        let input = document.getElementById('video_hidden');
        let label = document.getElementById('upload_video_label')
        label.innerHTML = input.files.item(0).name
    })

$(document).ready(function() {

// Initialized Uploaded filename
if (window.videoFN != ""){
    let label = document.getElementById('upload_video_label')
    label.innerHTML = window.videoFN
}

// EditorJS
let editorJsRaw = $("#description_hidden").val()
let editorJsJson

if (editorJsRaw != ""){
    editorJsJson = JSON.parse(editorJsRaw)
}

let editor = invokeEditorJS('description', editorJsJson)

$('#save').on('click', e => {
    editor.save().then((outputData) => {
        if (outputData.blocks.length != 0){
            let data = JSON.stringify(outputData)
            $('#description_hidden').val(data)
        }

        $('form').submit()

    }).catch((error) => {
    });
})

// Quest Dynamic Fields
function changeIndexQuestFields(fields, new_index, removeVal){
    fields.attr('id', 'quests-' + new_index + '-container')

    if (removeVal == true){
        fields.find('input[id$="-quest"]').val("")
    }
    fields.find('input[id$="-quest"]').attr('id', 'quests-' + new_index + '-quest')
    fields.find('input[name$="-quest"]').attr('name', 'quests-' + new_index + '-quest')

    if (removeVal == true){
        fields.find('input[id$="-answer"]').val('');
    }
    fields.find('input[id$="-answer"]').attr('id', 'quests-' + new_index + '-answer')
    fields.find('input[name$="-answer"]').attr('name', 'quests-' + new_index + '-answer')

    fields.find('img[id$="-x-btn"]').attr('id', 'quests-' + new_index + '-x-btn')

    fields.find('label[id$="-label"]').attr('id', 'quests-' + new_index + '-label')
    fields.find('label[id$="-label"]').html("Quest " + (new_index + 1))

    return fields
}

function reindexQuestFields(removeVal){
    let fields = $('div[data-type="quest-form-fields"]')
    $.each(fields, (index, value) => {
        changeIndexQuestFields($(value), index, removeVal)
    })

}

function setupQuestXBtn(){
    let xbtns = $('img[id^="quests-"][id$="-x-btn"]')

    $.each(xbtns, (index, value) => {
        let xbtn = $(value)
        xbtn.on('click', e => {
            if ($('div[data-type="quest-form-fields"]').length != 1){
                xbtn.parent().parent().remove()
                reindexQuestFields()
            }
        })
    })
}

//Add Quest Field
function cloneQuestFields(original, new_index){
    let clone = (original).clone()

    return changeIndexQuestFields(clone, new_index, true)
}

// Initialize X Buttons
setupQuestXBtn()

$('#add-quest').on('click', function(){
    let original = $('div[data-type="quest-form-fields"]:last')
    let new_index = parseInt(original.attr('id').split('-')[1]) + 1
    let clone = cloneQuestFields(original, new_index)
    $(clone).insertAfter(original)
    reindexQuestFields()
    setupQuestXBtn()
})


})

}
