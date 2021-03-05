$(document).ready(function () {
    $("#hero").click(function (e) {
        $("#menu-popup").fadeToggle("fast");
    });
});

$(document).mouseup(function (e) {
    let container = $("#menu-popup");
    let hero = $("#hero")
    if (!hero.is(e.target) &&
        !container.is(e.target) &&
        container.has(e.target).length === 0) {
        container.hide();
    }
});