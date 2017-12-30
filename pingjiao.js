// ==UserScript==
// @name         SCUEC评教
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  try to take over the world!
// @author       Justin
// @match        http://ssfw.scuec.edu.cn/ssfw/jxpg/xscx/pg.do?*
// @grant        none
// ==/UserScript==
/* 预置参数
* @param score 分数
* @param comment 评语
*/
var score = 10;
var comment = "老师讲课认真，一学期受益匪浅。";

var scoreRadio = document.querySelectorAll('.lx1>[value="1"]');
var saveButton = document.getElementsByClassName("saveButton")[0];

for (let i = scoreRadio.length - 1; i >= 0; i--) {
scoreRadio[i].click();
}

var evalTextBox = document.querySelectorAll('.lx3');
for (let i = evalTextBox.length - 1; i >= 0; i--) {
evalTextBox[i].value = comment;
}

var textBoxes = document.querySelectorAll(".lx10");
for(let i = textBoxes.length - 1; i >= 0; i--) {
    textBoxes[i].value = score;
}

function getNextButton() {
var nextButton = document.getElementById('nextlink');
return nextButton ? nextButton : false;
}

function jumpNext() {
if (getNextButton()) {
if ( saveButton.style.display != "none" ) {
saveButton.click();
return;
}
setTimeout(function() {
getNextButton().click();
setTimeout(function() {
jumpNext()
}, 100);
}, 0);
}
}

setTimeout(jumpNext(), 0);
