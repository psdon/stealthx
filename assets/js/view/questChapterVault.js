import invokeParticleWithSB from './particlesWithSidebar.js'
import { addEventByElementId } from '../script';
import invokeEditorJS from '../module/editor.js'

export default function createQuest() {

$(document).ready(function() {

invokeParticleWithSB();
addEventByElementId('upload_video_btn', 'click', (e) => {
    document.getElementById('video_hidden').click();
})

addEventByElementId('video_hidden', 'change', (e) => {
    let input = document.getElementById('video_hidden');
    let label = document.getElementById('upload_video_label')
    label.innerHTML = input.files.item(0).name
})

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

})

}