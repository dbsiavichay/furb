$(function () {
	$('#kind').on('change', function () {
		var kind = $(this).val();
		$.ajax('/breed/', {			
			data: {'kind': kind},
			success: function(data) {
				$('#id_breed').find('option:not(:first-child)').remove();
			    for (var i in data) {
			    	var option = '<option value="'+data[i].id+'">'+data[i].name+'</option>';
			    	$('#id_breed').append(option);
			    }
			},
			error: function(error) {
			    console.log(error)
			}
		});
	});
});