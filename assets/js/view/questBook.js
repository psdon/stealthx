import invokeParticleWithSB from './particlesWithSidebar.js'
import { addEventByElementId } from '../script';

export default function createQuest() {
    invokeParticleWithSB();

    addEventByElementId('avatar-upload-btn', 'click', (e) => {
        document.getElementById('avatar_hidden').click();
    })

    addEventByElementId('avatar_hidden', 'change', (e) => {
        let input = document.getElementById('avatar_hidden');
        let label = document.getElementById('avatar-file-label')
        label.innerHTML = input.files.item(0).name
    })

// Functions for Meta Tags

var tags = []

const tagContainer = document.getElementById('tag-container')
const tagInput = document.getElementById('tag-input')

function pushTagsToInput(){
    let hiddenInput = document.getElementById("meta_tags_hidden")
    hiddenInput.value = tags
}

function resetTags(){
    document.querySelectorAll('.tag-id').forEach((tag) => {
        tag.parentElement.removeChild(tag)
    })
}

function showTags(){
    resetTags()

    tags.slice().reverse().forEach((tag) => {
        tagContainer.prepend(createTag(tag))
    })
}

function createTag(label){
    const div = document.createElement('div')
    div.setAttribute('class', 'tag-id ml-2 text-base red-input font-normal border-1 rounded-xl flex items-center justify-center p-0 pl-3 pr-1 h-8')

    const span = document.createElement('span')
    span.innerHTML = label

    const closeBtn = document.createElement('img')
    closeBtn.setAttribute('class', 'tag-remove-id h-3 ml-1 cursor-pointer')
    closeBtn.setAttribute('src', window.xBtnLink)
    closeBtn.setAttribute('data-label', label)

    closeBtn.addEventListener('click', e => {
        const index = tags.indexOf(label)
        tags = [...tags.slice(0, index), ...tags.slice(index + 1)]
        showTags()
        pushTagsToInput()
    })

    div.appendChild(span)
    div.appendChild(closeBtn)
    return div
}

tagInput.addEventListener('keyup', (e) => {
    if (e.key == ","){
        const tagLabel = tagInput.value.replace(/,/g, "")
        tagInput.value = ''

        if (tagLabel != ""){
            tags.push(tagLabel)
            showTags()
            pushTagsToInput()
        }
    }
})

// Initialized Tags
let hiddenInput = document.getElementById("meta_tags_hidden")

if (hiddenInput.value == ""){
    tags.push("security")
    showTags()
    pushTagsToInput()
}else {
    tags = hiddenInput.value.split(",")
    showTags()
}

// Initialized Uploaded filename
if (window.avatarFN != ""){
    let label = document.getElementById('avatar-file-label')
    label.innerHTML = window.avatarFN
}

//prevent space
$('#quest_code').keypress(e => {
    let key = event.keyCode;
    if (key === 32) {
      return false
    }

    let string = String.fromCharCode(key)
    if (string.match(/[A-Z]/)) return false
})

// Chapter Delete Btn
$('button[data-type="chapter-delete-btn"]').each((i, obj) => {
    $(obj).on('click', e => {

        // Set Chapter Num
        let chapter_num = $(obj).attr("data-value")
        $('#modal-chapter-num').html(chapter_num)


        // Close Modal
        $("#modal-cancel-btn").on('click', (e) => {
             $('#modal-popup').addClass('hidden')
        })

        // Delete button
        let delete_route = window.dQCR.slice(0, -1) + chapter_num
        $("#modal-proceed-btn").attr("href", delete_route)

        // Show modal
        $('#modal-popup').removeClass("hidden")
    })
})

}