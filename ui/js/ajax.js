SERVER_URL = './httpAPI';

function run(str,model){
	result = [];
	$.ajax({async:false,url:SERVER_URL,type:'post',data:{'model':model,'text':str},dataType:'text',success:function(data,status){
			if (status!='success') return [];
			data = decodeURI(data.replace(new RegExp(/(%2C)/g),','));
			result = eval(data);
	}});
	return result;
}