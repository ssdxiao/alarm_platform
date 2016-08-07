/**
 * Created by lenovo on 2016/6/4.
 */
function get_custumer_list_refresh(index) {

    get_custumer_list(index, function (data) {
        var result = JSON.parse(data);
        console.log(result);
        if (result.result == "error") {
            console.log("获取用户列表失败")
        }
        else {
            //显示表信息
            $("#custumer_table tbody").empty();
            for (var i = 0; i < result.data.length; i++) {
                $("#custumer_table tbody").append("<tr class='default'> <td>" + result.data[i].custumerid +
                    "</td> <td>" + result.data[i].custumername + "</td> <td>" + result.data[i].custumertelephone +
                    "</td> <td>" + result.data[i].custumerdeviceid + "</td> </tr>")
            }

            $('#custumer_table tbody tr').each(function () {
                $(this).click(function (e) {
                    console.log("click custmer tr " + ($(this).text()).split(" ")[1]);
                    //用户详情信息写入
                    get_custumer($(this).text().split(" ")[4], function (data) {
                        var result = JSON.parse(data);
                        console.log(result);
                        if (result.result == "error") {
                            console.log("获取用户失败")
                        }
                        else {
                            $("#inputCustumerIdDetail").val(result.data.custumerid);
                            $("#inputCustumerNameDetail").val(result.data.custumername);
                            $("#inputCustumerTelephoneDetail").val(result.data.custumertelephone);
                            $("#inputCustumerEmailDetail").val(result.data.custumeremail);
                            $("#inputCustumerRemarkDetail").val(result.data.custumerremark);
                            $("#inputCustumerDeviceidDetail").val(result.data.deviceid);
                            $("#inputCustumerPhoneDetail").val(result.data.phone);
                            $("#inputCustumerStateDetail").val(result.data.state);
                            $("#inputCustumerCityDetail").val(result.data.city);
                            $("#inputCustumerStreetDetail").val(result.data.street);
                            $("#inputCustumerPostelCodeDetail").val(result.data.postelcode);
                            $("#Monleave").val(result.data.monleave);
                            $("#Monreturn").val(result.data.monreturn);
                            $("#Tueleave").val(result.data.tueleave);
                            $("#Tuereturn").val(result.data.tuereturn);
                             $("#Wedleave").val(result.data.wedleave);
                            $("#Wedreturn").val(result.data.wedreturn);
                            $("#Thuleave").val(result.data.thuleave);
                            $("#Thureturn").val(result.data.thureturn);
                            $("#Frileave").val(result.data.frileave);
                            $("#Frireturn").val(result.data.frireturn);
                            $("#Satleave").val(result.data.satleave);
                            $("#Satreturn").val(result.data.satreturn);
                            $("#Sunleave").val(result.data.sunleave);
                            $("#Sunreturn").val(result.data.sunreturn);
                            $("#Holleave").val(result.data.holleave);
                            $("#Holreturn").val(result.data.holreturn);


                            //处理other信息
                            $("#custumer_table_detail tbody").empty();
                            for (var i = 0; i < result.data.other.length; i++) {
                                insert_to_custumer_detail_table(result.data.other[i])

                            }
                        }

                    });
                    $("#custumer_detail").trigger("click")

                })
            });

            //显示分页条
           split_page("custumer", result, get_custumer_list_refresh);
        }

    })

}

function insert_to_custumer_detail_table(data) {
    $("#custumer_table_detail tbody").last().append("< class='default'><tr><td><input  name = 'name' type='text'class='input-medium' value='" + data.name +
        "'/></td> <td> <input name='token' type='text'class='input-medium' value='" + data.token + "'/></td> <td><input name='famliyphone' type='text'class='input-medium' value='" + data.famliyphone +
        "'/></td> <td><input name='workphone' type='text'class='input-medium' value='" + data.workphone + "'/></td> <td><input name='telphone' type='text'class='input-medium' value='" + data.telphone +
        "'/></td><td><a href=javascript:void(0); onclick=tr_del(event);return false;>删除</a></td>/tr>")
}

