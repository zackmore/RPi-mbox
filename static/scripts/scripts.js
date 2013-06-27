$(function(){

    var app = {
        songslist: '',
        playing: false,
        pid: '',

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
                console.log(this.songslist);
                // test code
                this.HTMLBlock.songsList(songsObj);
                //this.playASong(songsObj[0]);
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
                $('#song-image img').animate({'opacity': 0}, 400, 'ease-out',
                    function(){
                        $(this).attr(
                            {'src': '/static/mp3/images/'+songObj.imageurl,
                            'alt': songObj.name})
                        .animate({'opacity': 1}, 400, 'ease-in');
                    }
                );
            },
            songInfo: function(songObj){
                $('#song-name').html(songObj.name);
            }
        },

        playASong: function(songObj){
            app.playing = true;
            $.ajax({
                type: 'post',
                url: '/playnew',
                data: {
                    sid: songObj.sid,
                    pid: app.pid ? app.pid : ''
                },
                success: function(data){
                    app.pid = data;
                    console.log(app.pid);
                }
            });
            this.HTMLBlock.songImage(songObj);
            this.HTMLBlock.songInfo(songObj);
        },

        playAndPause: function(){
            $.ajax({
                type: 'post',
                url: '/playnew/control',
                success: function(data){
                    app.pid = data;
                    console.log(app.pid);
                }
            });
        },

        Stop: function(){
            $.ajax({
                type: 'post',
                url: '/playnew/control',
                success: function(data){
                    //
                }
            });
        },

        addNewSong: function(){
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
        app.playAndPause();
    });

    // songslist click and play
    $('#songslist a').live('click', function(e){
        e.preventDefault();
        $('#control a').attr('class', 'pause');
        var songindex = $(this).data('index');
        app.playASong(app.songslist[songindex]);
    });

    // stop
    $('#stop').click(function(e){
        e.preventDefault();
        app.Stop();
    });

    // add new song
    // open
    $('#newsong').click(function(e){
        e.preventDefault();
        $('#mask').addClass('show');
    });
    // submit
    $('#addnewsong input[type="submit"]').click(function(e){
        e.preventDefault();
        var form = $(this).parents('form');
        var postdata = form.serializeArray();
        console.log(postdata);
        $.ajax({
            type: 'post',
            url: '/addnewsong',
            data: postdata,
            success: function(data){
                console.log(data);
            }
        });
    });
    // close
    $('#closemask').click(function(e){
        e.preventDefault();
        $('#mask').removeClass('show');
    });

});
