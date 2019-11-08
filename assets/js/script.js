// App initialization code goes here

export function hasClass(ele, cls) {
    return ele.className.match(new RegExp('(\\s|^)' + cls + '(\\s|$)')) ? true: false;
}

export function addClass(ele, cls) {
    if (!hasClass(ele, cls)) ele.className += " " + cls;
}

export function removeClass(ele, cls) {
    if (hasClass(ele, cls)) {
        var reg = new RegExp('(\\s|^)' + cls + '(\\s|$)');
        ele.className = ele.className.replace(reg, ' ');
    }
}

export function showHide(id) {
       	let _element = document.getElementById(id);
       	hasClass(_element, "hidden") ? removeClass(_element, "hidden") : addClass(_element, "hidden");
}


export function addEventByElementId(elementId, evt, handler) {
    let _element = document.getElementById(elementId);
    _element.addEventListener(evt, function(event) {
        handler()
    });
}

