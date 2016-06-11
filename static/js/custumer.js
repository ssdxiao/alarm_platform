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
                    "</td> <td>" + result.data[i].custumerremark + "</td> </tr>")
            }

            $('#custumer_table tbody tr').each(function () {
                $(this).click(function (e) {
                    console.log("click custmer tr " + ($(this).text()).split(" ")[1]);
                    //用户详情信息写入
                    get_custumer($(this).text().split(" ")[1], function (data) {
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
    $("#custumer_table_detail tbody").last().append("< class='default'><tr><td><input  name = 'name' type='text'class='input-mini' value='" + data.name +
        "'/></td> <td> <input name='token' type='text'class='input-mini' value='" + data.token + "'/></td> <td><input name='famliyphone' type='text'class='input-mini' value='" + data.famliyphone +
        "'/></td> <td><input name='workphone' type='text'class='input-mini' value='" + data.workphone + "'/></td> <td><input name='telphone' type='text'class='input-mini' value='" + data.telphone +
        "'/></td><td><a href=javascript:void(0); onclick=tr_del(event);return false;>删除</a></td>/tr>")
}

