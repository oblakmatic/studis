$(function(){
    addID();
    
    $("#predmeti").on('change', addID);

    $("li.dropdown-l h5").on('click', expand);
});


function expand(){

    if ($(this).parents("li.dropdown-l:first").children("ul").is(':visible'))
        $(this).parents("li.dropdown-l:first").children("ul").hide();
    else
        $(this).parents("li.dropdown-l:first").children("ul").show();
}


function addID(){
    
    //preveri otroke in starse pri modulih
    $("input[name=modul-box]").on('change', function () {
        $(this).parents('li:first').children('ul')
               .find("input[type='checkbox']")
               .prop('checked', this.checked);
        

    });

    //pravilno število modulov
    modulParents=$("input[name=modul-box]");
    
    for (i =0; i < modulParents.size(); i++){
        if($("input[id=modul-"+i+"]").parents('li:first').children('ul').find("input[type='checkbox']:checked").size()==3){
            $("input[id=modul-"+i+"]").prop('checked', true);
        }
        else
            $("input[id=modul-"+i+"]").prop('checked', false);
    }

    modulCount=$('input[name=modul-box]:checked').size();
 
    //prestej izbrane predmete in seštej kt
    ids=[]
    count = 0
    $("input[name=izbran-predmet]:checked").each(function(){

        if($(this).is(":checked")){
            ids.push($(this).attr("id"));
            count+=$(this).data("kt")
        }
        
    });

    strokovenCount=0
    $("input[name=izbran-predmet]:checked").each(function(){

        if($(this).is(":checked") && $(this).data("st")=="True"){
            strokovenCount+=1;
        }
        
    });


    letnik = $("div.container.sifrant").data("letnik");
    prostaIzbira = $("div.container.sifrant").data("prosta");
    console.log(prostaIzbira)

    $("#vsi-id").val(ids);

    if (count== 60){

        if (letnik=="3." && modulCount!=2 && prostaIzbira=="False") {
            $("#notok").text("Izbrati je potrebno 2 modula.")
        }
        else if(letnik== "2." && strokovenCount < 1 )
            $("#notok").text("Izbrati je potrebno vsaj en strokoven predmet.")
        else {
        
            if ($("#ok").hasClass("d-none"))
                $("#ok").removeClass("d-none");

            if (! $("#notok").hasClass("d-none")){
                $("#notok").addClass("d-none");
            }
        }
    }
    else{
        $("#notok").text("Potrebnih je 60 kreditnih točk.")
        if (! $("#ok").hasClass("d-none")){
            $("#ok").addClass("d-none");
        }
        if ($("#notok").hasClass("d-none")){
            
            $("#notok").removeClass("d-none");
        }

    }

    $("#skupaj-kt-tock").text(count+"");
}