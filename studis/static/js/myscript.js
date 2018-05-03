
$(function(){
	addID();
	$("#predmeti").on('change', addID);
});

function addID(){

	//preveri otroke in starse pri modulih
	$("input[type='checkbox']").on('change', function () {
    $(this).siblings('ul')
           .find("input[type='checkbox']")
           .prop('checked', this.checked);
    $(this).closest('ul')
    	   .siblings('input:checkbox')
           .prop('checked', this.checked);
	});
      
    //prestej izbrane predmete
    ids=[]
    $("input[name=izbran-predmet]:checked").each(function(){
    	var $this = $(this);

	    if($this.is(":checked")){
	        ids.push($this.attr("id"));
	    }
	    else{

	    }
	});
    $("#vsi-id").val(ids);


   //prikazi primerno stevilo kt in sporocilo
  	izbranih = ids.length;
		
    skupaj = izbranih * 6 ;

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