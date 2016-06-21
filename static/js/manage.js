/**
 * Created by lenovo on 2016/6/4.
 */
function get_manage_list_refresh(index) {

    get_manage_list(index, function (data) {
        var result = JSON.parse(data);
        console.log(result);
        if (result.result == "error") {
            console.log("获取用户列表失败")
        }
        else {
            //显示表信息
            $("#manage_table tbody").empty();
            for (var i = 0; i < result.data.length; i++) {
                $("#manage_table tbody").append("<tr class='default'> <td>" + result.data[i].manageid +
                    "</td> <td>" + result.data[i].managename + "</td> <td>" + result.data[i].managetelephone +
                    "</td> <td>" + result.data[i].managelogintime + "</td> <td>" + result.data[i].managelogouttime +"</td> </tr>")
            }

            $("#manage_table tbody tr").each(function () {
                $(this).click(function (e) {
                    console.log("click custmer tr " + ($(this).text()).split(" ")[1]);
                    //用户详情信息写入
                    get_manage($(this).text().split(" ")[1], function (data) {
                        var result = JSON.parse(data);
                        console.log(result);
                        if (result.result == "error") {
                            console.log("获取用户失败")
                        }
                        else {
                            $("#inputManageIdDetail").val(result.data.manageid);
                            $("#inputManageNameDetail").val(result.data.managename);
                            $("#inputManageTelephoneDetail").val(result.data.managetelephone);
                            
                        }

                    });
                    $("#manage_detail").trigger("click")

                })
            });

            //显示分页条
           split_page("manage", result, get_manage_list_refresh);
        }

    })

}


