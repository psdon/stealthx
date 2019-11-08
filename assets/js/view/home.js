import { showHide, hasClass, addEventByElementId } from "../script"
import VimeoPlayer from "@vimeo/player"
import invokeParticles from "../module/invokeParticles"

export default function home(){

var player

function renderPlayer(){
    player = new VimeoPlayer("vimeo-player", {
        id: "362325129",
        responsive: true,
        autoplay: true
    });

    player.on("play", function() {
    let _element = document.getElementById("video-play-box");

    if (!hasClass(_element, "hidden")){
        showHide("video-play-box");
        showHide("video-reel-box");
    }

    });

    player.on("pause", function() {
        showHide("video-reel-box");
        showHide("video-play-box");
    });

}

invokeParticles("particles-1");
invokeParticles("particles-2");

let isRenderedPlayer = false

addEventByElementId("video-play-box", "click", function(e) {
    showHide("video-play-box");
    showHide("video-reel-box");

    if (isRenderedPlayer == false){
        renderPlayer()
        isRenderedPlayer = true;
    } else{
    player.play();
    }

});

}