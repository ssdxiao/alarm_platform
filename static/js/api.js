/**
 * Created by lenovo on 2016/5/11.
 */
function RestServiceJs(newurl) {
    this.myurl = newurl;

    this.post = function (model, callback) {
        $.ajax({
            type: 'POST',
            url: this.myurl,
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

    this.find = function (id, callback) {
        $.ajax({
            type: 'GET',
            url: this.myurl + '/' + id,
            contentType: 'application/json',
            success: callback,
            error: function (req, status, ex) {
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

function add_custumer(CustumerName, CustumerTelephone, CustumerEmail, CustumerRemark, callback) {
    url = new RestServiceJs("/app/custumer");
    var data = new Object();
    data.CustumerName = CustumerName;
    data.CustumerTelephone = CustumerTelephone;
    data.CustumerEmail = CustumerEmail;
    data.CustumerRemark = CustumerRemark;
    //console.log(JSON.stringify(data))
    url.post(data, callback)

}
function get_custumer_list(index,callback) {
    url = new RestServiceJs("/app/custumerlist?index="+index);
    url.findAll(callback)

}


function get_alarm_list(user) {
    url = new RestServiceJs("/app/alarm");
    var data = new Object();
    data.user = user;
    data.passwd = passwd;
    //console.log(JSON.stringify(data))
    url.post(data, callback)

}
