document.getElementById("prehistory").addEventListener("mouseenter", function() {
    document.getElementById("stone-label").classList.add("floating");
    document.getElementById("bronze-label").classList.add("floating");
    document.getElementById("iron-label").classList.add("floating");
});
document.getElementById("prehistory").addEventListener("mouseleave", function() {
    document.getElementById("stone-label").classList.remove("floating");
    document.getElementById("bronze-label").classList.remove("floating");
    document.getElementById("iron-label").classList.remove("floating");
});

document.getElementById("early-modern").addEventListener("mouseenter", function() {
    document.getElementById("renaissance-label").classList.add("floating");
    document.getElementById("industrial-label").classList.add("floating");
});
document.getElementById("early-modern").addEventListener("mouseleave", function() {
    document.getElementById("renaissance-label").classList.remove("floating");
    document.getElementById("industrial-label").classList.remove("floating");
});

document.getElementById("modern").addEventListener("mouseenter", function() {
    document.getElementById("twentieth-label").classList.add("floating");
    document.getElementById("atomic-label").classList.add("floating");
    document.getElementById("information-label").classList.add("floating");
});
document.getElementById("modern").addEventListener("mouseleave", function() {
    document.getElementById("twentieth-label").classList.remove("floating");
    document.getElementById("atomic-label").classList.remove("floating");
    document.getElementById("information-label").classList.remove("floating");
});