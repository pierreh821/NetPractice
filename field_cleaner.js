// ==UserScript==
// @name         Fields cleaner
// @version      2026-11-03
// @description  Cleans every free fields for NetPractice
// @author       pierreh821
// @match        http://localhost:49152/*
// @icon         https://www.google.com/s2/favicons?sz=64&domain=tampermonkey.net
// @grant        none
// ==/UserScript==

(function() {
    'use strict';

    var i;
    var inputs;

    inputs = document.getElementsByTagName('input');
    for (i = 0; i < inputs.length; ++i) {
        if (inputs[i].type != "button" && !inputs[i].disabled) {
            inputs[i].value = ""
        }
}
})();