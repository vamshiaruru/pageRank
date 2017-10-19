$(document).ready(function () {
    $('.reason').hide();
    $('.score').hide();
});
function hideClass(className) {
    $('.'+className).toggle();
}
function readFile(Filename) {
    var filename = Filename.children(0).attr('href');
    $.get(filename, function (data) {
        var win = window.open();
        win.document.open();
        var str =
        '<head>'+
        '<meta charset="UTF-8">'+
        '<title>Opened File!</title>'+
        '<script src="../static/js/jquery-3.2.1.min.js"></script>'+
        '<link rel="stylesheet" href="../static/css/openFile.css">'+
        '</head>'+
        '<body>';
        win.document.write(str);
        var lines = data.split("\n");
        win.document.write("<div class='article'>");
        win.document.write("<p class='title'>"+lines[0]+"</p>");
        for(var i = 1; i < lines.length; i++){
            win.document.write("<p>"+lines[i]+"</p>")
        }
        win.document.write("</div>");
        win.document.close();
    })
}