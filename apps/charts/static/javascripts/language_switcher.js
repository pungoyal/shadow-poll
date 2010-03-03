function switch_to_language(lang){
		$.post("/i18n/setlang/", {language : lang}, function(){
							 location.reload();
					 }
					);
}

