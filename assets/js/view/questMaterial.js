import invokeParticleWithSB from './particlesWithSidebar.js'
import { addEventByElementId } from '../script';

export default function createQuest() {
    invokeParticleWithSB();

    addEventByElementId('vm-file-upload-btn', 'click', (e) => {
        document.getElementById('vm-file-upload-input').click();
    })

    addEventByElementId('vm-file-upload-input', 'change', (e) => {
        let input = document.getElementById('vm-file-upload-input');
        let label = document.getElementById('vm-file-upload-label')
        label.innerHTML = input.files.item(0).name
    })

// Types Radio Buttons

var typeLegend = document.getElementById('type-legend')
let vmRadioBtn = document.getElementById('vm')
let downloadableFileRadioBtn = document.getElementById('downloadable-file')

vmRadioBtn.addEventListener('change', e => {
    if (e.target.checked){
        typeLegend.innerHTML = "( Accepted file types:  .ova,   .vmdk,   .vhd )"
    }
})

downloadableFileRadioBtn.addEventListener('change', e => {
    if (e.target.checked){
        typeLegend.innerHTML = "( Accepted file types:  Any file )"
    }
})


}