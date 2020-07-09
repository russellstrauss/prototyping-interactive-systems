$(function() {
	
	console.log('hello world :o');
	
	$.get('/dreams', function(dreams) {
		dreams.forEach(function(dream) {
			$('<li></li>').text(dream).appendTo('ul#dreams');
		});
	});

	$('form').submit(function(event) {
		event.preventDefault();
		let fname = $('input[name=fname]').val();
		let lname = $('input[name=lname]').val();
		let _age = $('input[name=age]').val();
		let _gender = $('input[name=gender]').val();
 
		let my_json = {firstname: fname, lastname: lname, age: _age, gender: _gender };
		console.log(my_json);
		
		$.ajax({
			type: "POST",
			url: "/dreams",
			// The key needs to match your method's input parameter (case-sensitive).
			data: JSON.stringify(my_json),
			contentType: "application/json; charset=utf-8",
			dataType: "json",
			success: function(dreams) {
				console.log("SUCCESS RETURNS");
				console.log(dreams);
				$('ul').empty();
				dreams.forEach(function(d) {
					$('<li></li>').text(d).appendTo('ul#dreams');
				});
			},
			failure: function(errMsg) {
					alert(errMsg);
			}
		});
	});
});
