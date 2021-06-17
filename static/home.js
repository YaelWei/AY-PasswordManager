$(document).ready(function () {
  //e.preventDefault();
  // var username = attr('data-pk').closest('td').prev('td').text();
  // console.log(username);

  $('#datatable').editable({
    container: 'body',
    selector: 'td.password',
    type: 'POST',
    url: '/editpassword',
    params: function (params) {
      var data = {};
      data['id'] = params.pk;
      data['value'] = params.value;
      data['username'] = $(this).closest('td').prev('td').text();
      data['website'] = $(this).parent().parent().find(".website").text();
      return data;
    }
  });

  $("tbody").click((e) => {
    if (e.target instanceof HTMLAnchorElement && e.target.classList.contains("copy-password")) {
      e.preventDefault();
      const password = $(e.target).closest('td').prev('td').text();
      navigator
        .clipboard
        .writeText(password)
        .catch((err) => {
          /* clipboard write failed */
          console.log("Copy failed.", err.message);
        });
    }
  });


  $("#add-entry").click(function (e) {
    e.preventDefault();

    var id = $('#id').val(), password = $('#password').val(), username = $('#username').val(), website = $('#website').val();
    // var $buttonToAdd = $('<td></td>');

    $("#datatable").append(
      "<tbody>" + "<tr>" +
      "<td data-pk='" + $('#id').val() + "'class='id'>" + $("#id").val() + "</td>" +
      "<td data-name='website' data-pk='" + $('#id').val() + "' class='website'>" + $("#website").val() + "</td>" +
      "<td data-name='username'data-pk='" + $('#id').val() + "' class='username'>" + $("#username").val() + "</td>" +
      "<td data-name='password' data-type='text' data-pk='" + $('#id').val() + "' class='password'>" + $("#password").val() + "</td>" +
      "<td id='buttonToAdd'>" + "</td>" +
      "</tr>" + "</tbody>");

    $.ajax({
      url: '/addpassword',
      type: 'POST',
      data: {
        id: id,
        value: password,
        username: username,
        website: website
      },
      success: function (response) {


        document.querySelector('#buttonToAdd').insertAdjacentHTML('afterbegin', `<td>
            <div class="btn-group dropright">
                <button type="button" class="btn dropdown-toggle" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                    <i class="fas fa-ellipsis-h"></i>
                </button>
                <div class="dropdown-menu" x-placement="right-start" style="position: absolute; transform: translate3d(111px, 0px, 0px); top: 0px; left: 0px; will-change: transform;">
                    <a class="dropdown-item copy-password" id='${$('#id').val()}'>Copy Password</a>
                    <a class="dropdown-item delete-password" id=${$('#id').val()}>Delete Record</a>
                </div>
              </div>
        </td>`);

        //clearing the form
        $("#id").val("");
        $("#website").val("");
        $("#username").val("");
        $("#password").val("");
        window.location.reload();


      }
    });

  });


  //when you click on delete, it should delete the whole role
  //should we verify that the user wants to delete?
  $(".delete-password").click(function (e) {
    e.preventDefault();
    // var deleteid = $(this).data('id');
    var $tr = $(this).closest('tr');
    // AJAX Request
    $.ajax({
      url: '/deletepassword',
      type: 'POST',
      data: {
        id: $(this).closest('tr').children('td:first').text(),
        value: $(this).closest('td').prev('td').text(),
        username: $(this).closest('td').prev('td').prev('td').text(),
        website: $(this).closest('td').prev('td').prev('td').prev('td').text()
      },
      success: function (response) {
        // $("#datatable").html(response);
        // $(this).closest('td').parents('tr');

        // Remove row from HTML Table
        // alert($(this).closest('td').parents('tr'));
        $tr.css('background', 'tomato');
        $tr.fadeOut(800, function () {
          $tr.remove();
        });

      }
    });
  });


});
 // var dataTable = $('#datatable').DataTable();

  // $("#delete-entry").click(function(){
  //   $.ajax({
  //     type: 'POST',
  //     url: "/_delete_entry",
  //     data: {student_id: 1},
  //     dataType: "text",
  //     success: function(data){
  //                alert("Deleted Student ID "+ student_id.toString());
  //              }
  //   });
  // });

//  $(".edit-password").click(function(){
//     document.getElementsByClassName().readOnly=true;