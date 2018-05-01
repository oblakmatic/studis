
$(function(){
	preveriPredmete();

	$("#izbirni-predmeti").click(preveriPredmete);
	$("#modul-predmeti").click(preveriPredmete);


	$("input[type='checkbox']").on('change', function () {
     $(this).siblings('ul')
           .find("input[type='checkbox']")
           .prop('checked', this.checked);
     console.log($(this).siblings('ul')
           .find("input[type='checkbox']")
           .prop('checked', this.checked).length)
  });
});

function preveriPredmete(){

		base_value = $("#predmeti").data("base");

		izbranih = $('#izbirni-predmeti :input[type="checkbox"]:checked');
	    
	    izbranih2 = $('#modul-predmeti :input[type="checkbox"]:checked');

	
	    skupaj = base_value + izbranih.length *6 + izbranih2.length * 18;

	    if (skupaj== 60){

	    	if ($("#ok").hasClass("d-none"))
	    		$("#ok").removeClass("d-none");

	    	if (! $("#notok").hasClass("d-none")){
	    		$("#notok").addClass("d-none");
	    	}
	    }
	    else{
	    	if (! $("#ok").hasClass("d-none")){
	    		$("#ok").addClass("d-none");
	    	}
	    	if ($("#notok").hasClass("d-none"))
	    		$("#notok").removeClass("d-none");

	    }

	    $("#skupaj-kt-tock").text(skupaj+"");
}