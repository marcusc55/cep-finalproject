$(document).ready(function() {
  $('#suggestion').keyup(function(){
    var query;
    query = $(this).val();
    $.ajax({     
      method:'post',
      url:'/gameangel/suggest_game/', 
      data: {
        'csrfmiddlewaretoken': $.cookie("csrftoken"), 
        'suggestion': query,
      }, 
      success:function(data){
            $('#cats').html(data);
          }
    });  
  });
});