/**
 * Created by lenovo on 2016/5/11.
 */
function RestServiceJs(newurl) {
    this.myurl = newurl;

    this.post = function (model, callback) {
        $.ajax({
            type: 'POST',
            url: this.myurl,
            beforeSend: function (request) {
                request.setRequestHeader("X-Auth", getCookie("user"));
            },
            data: JSON.stringify(model), // '{"name":"' + model.name + '"}',  
            dataType: 'text',
            processData: false,
            contentType: 'application/json',
            success: callback,
            error: function (req, status, ex) {

            },
            timeout: 60000
        });
    };

    this.put = function (model, callback) {
        $.ajax({
            type: 'PUT',
            url: this.myurl,
            beforeSend: function (request) {
                request.setRequestHeader("X-Auth", getCookie("user"));
            },
            data: JSON.stringify(model), // '{"name":"' + model.name + '"}',  
            dataType: 'text',
            processData: false,
            contentType: 'application/json',
            success: callback,
            error: function (req, status, ex) {
                 alert("请检查输入内容是否正确")

            },
            timeout: 60000
        });
    };

    this.find = function (callback) {
        $.ajax({
            type: 'GET',
            url: this.myurl,
            beforeSend: function (request) {
                request.setRequestHeader("X-Auth", getCookie("user"));
            },
            contentType: 'application/json',
            success: callback,
            error: function (req, status, ex) {

            },
            timeout: 60000
        });
    };
    this.telephone_use = function (callback,server) {
        $.ajax({
            type: 'GET',
            url: this.myurl,
            dataType: 'JSONP',
            success: callback,
            error: function (req, status, ex) {
                console.log(req.getAllResponseHeaders())
                console.log(status)
                console.log(ex)
                if (status == "timeout"){
                    alert("请检查电话服务是否启动")
                }
                if (status == "error"){
                    if("undefined" == typeof server)
                    {
                        server=""
                    }
                    alert("请检查"+server+"服务是否正常")
                }
            },
            timeout: 60000
        });
    };

    this.findAll = function (callback) {
        //alert('sfindall');  
        //alert('myurl' + this.myurl);  

        $.ajax({
            type: 'GET',
            url: this.myurl,
            beforeSend: function (request) {
                request.setRequestHeader("X-Auth", getCookie("user"));
            },
            contentType: 'application/json',
            success: callback,
            error: function (req, status, ex) {
            },
            timeout: 60000
        });
    };

    this.remove = function (id, callback) {
        $.ajax({
            type: 'DELETE',
            url: this.myurl + '/' + id,
            beforeSend: function (request) {
                request.setRequestHeader("X-Auth", getCookie("user"));
            },
            contentType: 'application/json',
            success: callback,
            error: function (req, status, ex) {
            },
            timeout: 60000
        });
    };

    this.loadTmpl = function (turl, callback) {
        $.ajax({
            url: turl,
            success: callback,
            error: function (req, status, ex) {
            },
            timeout: 60000
        });
    }
};


function setCookie(name, value) {
    var Days = 1;
    var exp = new Date();
    exp.setTime(exp.getTime() + Days * 24 * 60 * 60 * 1000);
    document.cookie = name + "=" + escape(value) + ";expires=" + exp.toGMTString();
}
//读取cookies
function getCookie(name) {
    var arr, reg = new RegExp("(^| )" + name + "=([^;]*)(;|$)");
    if (arr = document.cookie.match(reg)) return unescape(arr[2]);
    else return null;
}
//删除cookies
function delCookie(name) {
    var exp = new Date();
    exp.setTime(exp.getTime() - 1);
    var cval = getCookie(name);
    if (cval != null) document.cookie = name + "=" + cval + ";expires=" + exp.toGMTString();
}


function login(user, passwd, callback) {
    url = new RestServiceJs("/app/login");
    var data = new Object();
    data.user = user;
    data.passwd = passwd;
    //console.log(JSON.stringify(data))
    url.post(data, callback)

}

function logout(user, token) {
    url = new RestServiceJs("/app/logout");
    var data = new Object();
    data.user = user;
    data.token = token;
    //console.log(JSON.stringify(data))
    url.post(data, function (data) {

    })

}

function add_custumer(CustumerName, CustumerTelephone, CustumerEmail, CustumerRemark, CustumserDeviceid,callback) {
    url = new RestServiceJs("/app/custumer");
    var data = new Object();
    data.CustumerName = CustumerName;
    data.CustumerTelephone = CustumerTelephone;
    data.CustumerEmail = CustumerEmail;
    data.CustumerRemark = CustumerRemark;
    data.CustumerDeviceid = CustumserDeviceid;
    //console.log(JSON.stringify(data))
    url.post(data, callback)

}

function add_manage(ManageName, ManageTelephone, ManagePassword, callback) {
    url = new RestServiceJs("/app/manage");
    var data = new Object();
    data.ManageName = ManageName;
    data.ManageTelephone = ManageTelephone;
    data.ManagePassword = ManagePassword;

    //console.log(JSON.stringify(data))
    url.post(data, callback)

}

function get_manage(ID, callback) {
    url = new RestServiceJs("/app/manage?id=" + ID);
    url.find(callback)
}

function get_manage_list(index, callback) {
    url = new RestServiceJs("/app/managelist?index=" + index);
    url.findAll(callback)

}


function get_custumer(CustumerID, callback) {
    url = new RestServiceJs("/app/custumer?id=" + CustumerID);
    url.find(callback)
}
function get_event_list(alarmid, callback){
    url = new RestServiceJs("/app/events?alarmid=" + alarmid);
    url.find(callback)
}

function update_custumer(data, callback) {
    url = new RestServiceJs("/app/custumer")
    url.put(data, callback)
}

function update_manage(data, callback) {
    url = new RestServiceJs("/app/manage")
    url.put(data, callback)
}

function update_manage_passwd(data, callback) {
    url = new RestServiceJs("/app/manage/changepasswd")
    url.put(data, callback)
}

function get_record_list(index, callback) {
    url = new RestServiceJs("/app/recordlist?index=" + index);
    url.findAll(callback)

}
function update_alarm(data, callback) {
    url = new RestServiceJs("/app/alarm")
    url.put(data, callback)
}

function release_alarm(data, callback) {
    url = new RestServiceJs("/server/releasealarm")
    url.post(data, callback)
}

function get_custumer_list(index, callback) {
    url = new RestServiceJs("/app/custumerlist?index=" + index);
    url.findAll(callback)

}


function get_alarm(CustumerID, callback) {
    url = new RestServiceJs("/app/alarm?id=" + CustumerID);
    url.find(callback)
}

function get_alarm_list(index, callback) {
    url = new RestServiceJs("/app/alarmlist?index=" + index);
    url.findAll(callback)

}


function tr_del(e) {
    console.log($(e.currentTarget).parent())
    console.log("delete tr")
    $(e.currentTarget).parent().parent().remove();
}
function do_call(alarmid, telephone, callback) {
    url = new RestServiceJs("http://localhost:8080/callout.html?u="+alarmid+"&c="+telephone);
    //window.location.href="http://localhost:8080/callout.html?u="+alarmid+"&c="+telephone
    url.telephone_use(callback, "电话")


}

function do_hangup( callback) {
    $("#deal_message").text("挂机")
    url = new RestServiceJs("http://localhost:8080/hangup.html")
    url.telephone_use(callback, "电话")
}

function callup(e) {
    if ($("#deal_progress").text() == alarm_string[2]) {
        return
    }
    var telephone = $(e.currentTarget).text();

    if (telephone == "")
    {
        return
    }
    var timestamp = Date.parse(new Date());
    window.alarm_audio = $("#td_alarm_id").text()+"+"+timestamp;
    window.alarm_telephone = telephone
    $("#deal_message").text("电话中...")
    $("#audiofile_message").text("本次录音文件为 " + window.alarm_audio + ".wav")
    console.log("callup")
    do_call(window.alarm_audio, telephone, function (data){
        //data = JSON.parse(data)
        if(data.msg != "OK"){
                        alert(data.msg)
        }
        console.log("call callon api return")
        console.log(data)


    })
    $("#modal_alarm_detail").modal('hide')
    $('#modal_alarm_deal').modal({backdrop: 'static'})
    //$("#alarm_deal").trigger("click")

}


function commit_alarm_record(alarmid, telephone, remark, audio, callback) {
    url = new RestServiceJs("/app/audio");
    var data = new Object();
    data.AlarmID = alarmid;
    data.AlarmRemark = remark;
    data.AlarmAudio = audio;
    data.AlarmTelephone = telephone;

    console.log(JSON.stringify(data))
    url.post(data, callback)

}
function get_audio_list(alarm_id, callback) {
    url = new RestServiceJs("/app/audiolist?alarm=" + alarm_id)
    url.findAll(callback)

}


function split_page(name, result, fresh_function) {
    window.current_page = result.curruntindex;
    $("#" + name + "_page ul").empty();
    $("#" + name + "_page ul").append("<li> <a >上一页</a> </li>");
    var start_index = 0;
    var end_index = 0;
    if (result.curruntindex > 3) {
        var start_index = result.curruntindex - 3

    }
    var diff = result.maxindex - result.curruntindex
    if (diff > 3) {
        end_index = result.curruntindex + 3
        if (result.curruntindex < 3) {
            end_index = end_index + 3 - result.curruntindex
        }
        if (end_index > result.maxindex) {
            end_index = result.maxindex;
        }
    }
    else {
        end_index = result.maxindex;

        start_index = start_index - 3 + diff;
        if (start_index < 0) {
            start_index = 0

        }

    }

    for (var i = start_index; i < end_index; i++) {
        if (i+1 == result.curruntindex)
        {
        $("#" + name + "_page ul").append("<li class='disabled'> <a>" + (i + 1) + "</a> </li>");
        }
        else{
        $("#" + name + "_page ul").append("<li> <a >" + (i + 1) + "</a> </li>");
        }
    }
    $("#" + name + "_page ul").append("<li> <a >下一页</a> </li>");

    $("#" + name + "_page").attr("style", "display:''");
    $("#" + name + "_page ul a").each(function () {
        $(this).click(function (e) {
            var index;
            if ($(this).text() == "上一页") {
                index = window.current_page - 1;
            }
            else if ($(this).text() == "下一页") {
                index = window.current_page + 1;
            }
            else {
                index = $(this).text();
            }
            fresh_function(index)
        })
    })
}

function get_userid() {
    var value = getCookie("user");
    if (value) {
        var data = JSON.parse(value);
        if (typeof(data.user) != "undefined") {
            console.log(data)
            return data.id
        }
        else {
            return
        }
    }
}

function ajaxFileUpload( id) {
    console.log("ajaxFileUpload")
    $.ajaxFileUpload({
        url: '/app/upload',
        secureuri: true,
        fileElementId: id,
        dataType: 'json',
        success: function (data, status) {
            console.log("upload success")
            if (typeof(data.error) != 'undefined') {
                if (data.error != '') {
                    console.log(data.error)
                }
                else {
                    console.log("upload ok")
                }
            }
        },
        error: function (data, status, e) {
            console.log("return value error");
        }
    })
    return false;
}

function upload_model(e){
    var id = e.currentTarget.id
    $("#upload_message").text(id)
    //$("#modal_alarm_detail").attr("style", "display:none")
     $("#modal_alarm_detail").modal('hide')
    $("#upload").trigger("click")
}
  
//播放暂停切换  
function playAudio(e) {
    console.log("play audio")
    var media = e.currentTarget.parentNode.firstChild
    if(media.paused) {  
        play(media);
    } else {  
        pause(media);
    }  
}  
  
//播放  
function play(media) {
    media.play();
}  
  
//暂停  
function pause(media) {
    media.pause();  

}  


function getFileName(o){
    var pos=o.lastIndexOf("\\");
    return o.substring(pos+1);  
}
