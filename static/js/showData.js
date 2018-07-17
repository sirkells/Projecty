var pagenoVar = 0;
var pagenoPrevious = 0;
var limit = 5;
var currentPage = 1


function pageSizeModifier() {
  $('#pageSize').bind("enterKey", function(e) {
    //do stuff here
    $("#nextButton").html("asdf")
  });
}

var displayText = function(data) {
  var new_tbody = document.createElement('tbody');
  console.log(data.length);
  data.forEach(function(item) {
    $(new_tbody).append("<tr>" + "<td>" + item["time"] + "</td>" + "<td>" + item["ipAddress"] + "</td>" + "<td>" + item["question"] + "</td>" + "<td><textarea rows=5 cols=40>" + item["answer"] + "</textarea></td>" + "</tr>")
  });
  $(new_tbody).attr('id', "showDataBody");
  $("#showDataBody").replaceWith(new_tbody);
}

var successRoutes = function(response) {
  console.log("response  = " + response)

  console.log("in successRoutes")
  responseData = response.data
  // responseParams = response.param
  pagenoVar = response.param["pageno"]
  // console.log(responseParams);
  if (responseData.length < $("#pageSize").val()) {
    $("#nextButton").prop("disabled", true);
    displayText(responseData)

  } else {
    $("#nextButton").prop("disabled", false);
    displayText(responseData)
  }
}

function makeAjaxCall(obj) {
  // var queryType = $('input[name=queryType]:checked').val();
  // var limit = $("#pageSize").val();

  var whichButton = $(obj).attr("id");

  console.log(whichButton);
  // console.log(whichButton);

  if (whichButton == undefined) {
    // pagenoVar = 0;
    // pagenoPrevious = 0;
    whichButton = "undefined"
  } else if (whichButton == "previousButton") {
    currentPage = currentPage - 1
    pagenoVar = pagenoPrevious - limit
  } else if (whichButton == "nextButton") {
    currentPage = currentPage + 1

    // pagenoVar = pagenoVar + limit
  } else if (whichButton == "pageSize") {
    pagenoVar = pagenoPrevious
  }
  if (pagenoVar < 0) {
    pagenoVar = 0
    currentPage = 1
  }
  pagenoPrevious = pagenoVar

  $("#DisplayPageNo").html(currentPage)
  var pageSize = $("#pageSize").val()

  $.ajax({
    url: '/api/getAllData',
    data: JSON.stringify({
      "pageno": pagenoVar,
      "pageSize": pageSize,
      "queryType": queryType,
      "moveDirection": whichButton
    }),
    type: 'POST',
    contentType: 'application/json; charset=utf-8',
    datatype: "json",
    success: successRoutes,
    error: function() {
      console.log("it man")
    },
  });
}

$(document).ready(function() {

  makeAjaxCall()
  var limit = $("#pageSize").val();

  $("input:radio[name='queryType']").change(function() {
    pagenoVar = 0
    currentPage = 0
    pagenoPrevious = 0
    $("#nextButton").prop("disabled", false);
    makeAjaxCall($("#nextButton"));

  });


});
