function getCookie(e){var t=null;if(document.cookie&&""!=document.cookie)for(var o=document.cookie.split(";"),n=0;n<o.length;n+=1){var r=jQuery.trim(o[n]);if(r.substring(0,e.length+1)==e+"="){t=decodeURIComponent(r.substring(e.length+1));break}}return t}function csrfSafeMethod(e){return/^(GET|HEAD|OPTIONS|TRACE)$/.test(e)}$.ajaxSetup({beforeSend:function(e,t){csrfSafeMethod(t.type)||this.crossDomain||e.setRequestHeader("X-CSRFToken",getCookie("csrftoken"))}});