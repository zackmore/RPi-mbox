$(function(){

    var app = {
        songslist: '',
        playing: false,

        getListId: function(){
            var url = window.location.href;
            if(url.indexOf('#')){
                var listid = url.split('#')[1];
            }
            return listid ? listid : 1; 
        },

        getJSON: function(listid){
            var tmp = {};
            var url = '/list/' + listid;
            $.getJSON(url, function(data){
                app.songslist = data;
                app.JSONtoHTML(data);
            });
        },

        JSONtoHTML: function(songsObj){
            if(songsObj.length){
                this.songslist = songsObj;
                // test code
                this.HTMLBlock.songsList(songsObj);
                this.playASong(songsObj[0]);
            }else{
                $('#song-name').html('Erro occurs, please try again later.');
            }
        },

        HTMLBlock: {
            songsList: function(songsObj){
                for(var i=0; i<songsObj.length; i++){
                    var songurl = songsObj[i].sid;
                    var songname = songsObj[i].name;
                    var songorder = (i+1).toString() + '.';
                    var li = $('<li><a></a></li>');
                    li.find('a').attr('href', songurl)
                    .attr('data-index', i)
                    .html(songorder+' '+songname);
                    li.appendTo($('#songslist'));
                }
            },
            songImage: function(songObj){
                $('#song-image img').animate({'opacity': 0}, 400, function(){
                    this.remove();
                });

                $('<img>').attr({'src': '/static/mp3/images/'+songObj.imageurl, 'alt': songObj.name})
                .css({'opacity': 0})
                .appendTo($('#song-image'))
                .animate({'opacity': 1}, 500);
            },
            songInfo: function(songObj){
                $('#song-name').html(songObj.name);
            }
        },

        playASong: function(songObj){
            // todo: send a stop command to mplayer
            this.HTMLBlock.songImage(songObj);
            this.HTMLBlock.songInfo(songObj);
            // todo: send a play command to mplayer
        },

        init: function(){
            this.getJSON(this.getListId());
        }
    };

    app.init();

    // play and pause
    $('#control a').click(function(e){
        e.preventDefault();
        $(this).toggleClass('pause');
    });

    // songslist click and play
    $('#songslist a').live('click', function(e){
        e.preventDefault();
        var songindex = $(this).data('index');
        app.playASong(app.songslist[songindex]);
    });
});
