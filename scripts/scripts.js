$(function(){
    var mp3files = [
        {"name": "1", "url": "1.mp3", "img": "1.jpg"},
        {"name": "2", "url": "2.mp3", "img": "2.jpg"},
        {"name": "3", "url": "3.mp3", "img": "3.jpg"}
    ];
    console.log(mp3files);

    $('#control a').click(function(e){
        $(this).toggleClass('pause');
    });
});
