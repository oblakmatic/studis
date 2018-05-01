
$(function(){
	preveriPredmete();
	$("#izbirni-predmeti").click(preveriPredmete);
	$("#modul-predmeti").click(preveriPredmete);
});

function preveriPredmete(){

		base_value = $("#predmeti").data("base");

		izbranih = $('#izbirni-predmeti :input[type="checkbox"]:checked').length;
	    
	    izbranih2 = $('#modul-predmeti :input[type="checkbox"]:checked').length;
	
	    skupaj = base_value + izbranih *6 + izbranih2 * 18;

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