$(document).ready(function(){
	colors = ["FFFFCC","FFCCFF","CCFFFF","FFCCCC","CCFFCC","CCCCFF","FFCC99","FF99CC","CCFF99"]
	html = ''
	for (var i=0;i<colors.length;i++) html += '.color-'+colors[i]+'{background-color:#'+colors[i]+'; border-style:none;}\n';
	$("#css-colors").html(html);
	
	$(".left-button").click(function(){
		id = $(this).attr('id');
		$('#input-model').html(id);
		$('.left-button-clicked').removeClass('left-button-clicked').addClass('left-button-unclicked');
		$('#'+id).addClass('left-button-clicked');
	});
	
	$("#center-button-clear").click(function(){
	    $("#center-button-edit").removeClass("center-button-good");
		$("#center-button-edit").addClass("center-button-bad");
		$("#center-button-run").removeClass("center-button-bad");
		$("#center-button-run").addClass("center-button-good");
		$("#id-label-area").html('');
		$("#display-text").css("display","none");
		$("#input-text").css("display","block");
		$("#input-text").val("");
	});
   
	$("#center-button-edit").click(function(){
		if($("#center-button-edit").hasClass("center-button-bad")) return;
		$("#center-button-edit").removeClass("center-button-good");
		$("#center-button-edit").addClass("center-button-bad");
		$("#center-button-run").removeClass("center-button-bad");
		$("#center-button-run").addClass("center-button-good");
		$("#id-label-area").html('');
		$("#display-text").css("display","none");
		$("#input-text").css("display","block");
	}); 
	
	BUTTON_RUN_ERROR = "未检测出任何关键词";
	RESULT_MORE_THAN_9_ERROR = "识别输出超过九种，前端出错"
	$("#center-button-run").click(function(){
		if($("#center-button-run").hasClass("center-button-bad")) return;
		str = $("#input-text").val();
		model = $("#input-model").html();
		if (str=="") return alert(BUTTON_RUN_ERROR);
		
		result = run(str,model);
		if (result.length==0) return alert(BUTTON_RUN_ERROR);
		
		d = {};
		now_color = 0;
		html = ''
		for (var i=0;i<result.length;i++){
			if (d[result[i][2]]==undefined){
				if (now_color >= colors.length){
					alert(RESULT_MORE_THAN_9_ERROR);
					return;
				}
				d[result[i][2]] = colors[now_color];
				html = $("#id-label-area").html();
				html += '<div class="id-label" name="'+d[result[i][2]]+'">'+result[i][2]+'</div>';
				$("#id-label-area").html(html);
				now_color++;
			}
		}
		
		$(".id-label").each(function(){$(this).addClass("color-"+$(this).attr("name"));});
		$(".id-label").click(function(){
			colorname = $(this).attr('name')
			classname = 'color-'+colorname;
			if ($(this).hasClass(classname))
				$('.'+classname).removeClass(classname).addClass('un'+classname);
			else
				$('.un'+classname).removeClass('un'+classname).addClass(classname);
		});
		
		r = '';
		for (var i=0;i<str.length;i++) r += '<span id="text-'+i.toString()+'">'+str[i]+'</span>';
		$("#display-text").html(r);
		
		result.sort(function(a,b){ return (a[1]-a[0])-(b[1]-b[0]); });
		for (var i=0;i<result.length;i++){
			for (var j=result[i][0];j<result[i][1];j++)
				$("#text-"+j.toString()).addClass("color-"+d[result[i][2]]);
		}
		
		
		$("#center-button-run").removeClass("center-button-good");
		$("#center-button-run").addClass("center-button-bad");
		$("#center-button-edit").removeClass("center-button-bad");
		$("#center-button-edit").addClass("center-button-good");
		$("#input-text").css("display","none");
		$("#display-text").css("display","block");
	}); 
	
	$("#center-button-uploadfile").click(function(){
		$('#input-file').val('');
		$('#input-file').click();
	});
	
	$('#input-file').change(function(){
		var file = document.getElementById("input-file").files[0];  
		var reader = new FileReader();
		reader.onloadend = function(e){
			$('#input-text').val(e.target.result);
		}
		reader.readAsText(file);  
	});
});