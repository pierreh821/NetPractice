inputs = document.getElementsByTagName('input');
for (i = 0; i < inputs.length; ++i) {
    if (inputs[i].type != "button" && !inputs[i].disabled) {
        inputs[i].value = ""
    }
}