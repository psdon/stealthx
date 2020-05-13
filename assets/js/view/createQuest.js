import invokeParticleWithSB from './particlesWithSidebar.js'
import { addEventByElementId } from '../script';

export default function createQuest() {
    invokeParticleWithSB();

    addEventByElementId('avatar-upload-btn', 'click', (e) => {
        document.getElementById('avatar-upload-input').click();
    })

    addEventByElementId('avatar-upload-input', 'change', (e) => {
        let input = document.getElementById('avatar-upload-input');
        let label = document.getElementById('avatar-file-label')
        label.innerHTML = input.files.item(0).name
    })

    addEventByElementId('vm-file-upload-btn', 'click', (e) => {
        document.getElementById('vm-file-upload-input').click();
    })

    addEventByElementId('vm-file-upload-input', 'change', (e) => {
        let input = document.getElementById('vm-file-upload-input');
        let label = document.getElementById('vm-file-upload-label')
        label.innerHTML = input.files.item(0).name
    })

// Functions for Meta Tags

var tags = []

const tagContainer = document.getElementById('tag-container')
const tagInput = document.getElementById('tag-input')

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
        }
    }
})


}