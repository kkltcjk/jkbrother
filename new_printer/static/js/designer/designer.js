$(document).ready(function() {
	var works_wait_btn = $('#works_wait_btn'),//未审核
		works_on_btn = $('#works_on_btn'),//审核中
		works_not_btn = $('#works_not_btn'),//未通过
		works_Suc_btn = $('#works_Suc_btn');//已发布
		designer_works_lists = $('.designer-works-lists');

	works_wait_btn.on('click',function(){//未审核页面
		designer_works_lists.empty();
		var waitStr = '';
	});

	works_on_btn.on('click',function(){//审核中页面
		designer_works_lists.empty();
		var onStr='';
		$.post('designer/photo_on_review',{"page":1}, function(e) {
			if(e){
				var onList = JSON.parse(e).list;
				for(var i=0,len=onList.length;i<len;i++){
					onStr+='<div class="designer-works-list-box clearfix"><div class="designer-works-list-bigpic fl"><img src="'+onList[i].bigPic+'"/></div><div class="designer-works-list-detail fl"><p class="designer-works-list-title">"'+onList[i].name+'"</p><p class="designer-works-list-describe">'+onList[i].describe+'</p><div class="designer-works-list-pics clearfix">';
					for(var j=0,jlen=onList[i].pic.length;j<jlen;j++){
						waitStr +='<img src="'+onList[i].pic[j]+'"/>';
					}
					onStr +='</div></div><div class="designer-works-list-status fl"><strong>审核中···</strong><p>您的作品预计在'+onList[i].restdate+'天内被审核完毕并发布。</p></div></div>';
				}
			}else{
				onStr='信息加载失败..';
			}
			designer_works_lists.append(onStr);
		});
	});

	works_Suc_btn.on('click',function(){//已发布页面
		designer_works_lists.empty();
		var sucStr ='';
		$.post('designer/photo_success_pubulic',{"page":1}, function(e) {
			if(e){
				var sucList = JSON.parse(e).list;
				for(var i=0,len=sucList.length;i<len;i++){
					sucList+='<div class="designer-works-list-box clearfix"><div class="designer-works-list-bigpic fl"><img src="'+sucList[i].bigPic+'"/></div><div class="designer-works-list-detail fl"><p class="designer-works-list-title">"'+sucList[i].name+'"</p><p class="designer-works-list-describe">'+sucList[i].describe+'</p><div class="designer-works-list-pics clearfix">';
					for(var j=0,jlen=sucList[i].pic.length;j<jlen;j++){
						sucList +='<img src="'+sucList[i].pic[j]+'"/>';
					}
					sucStr +='</div></div><div class="designer-works-list-data fl"><div class="list-data-container clearfix"><div class="list-data-box fl"><span class="list-data-num list-download-num">'+sucList[i].downloadNum+'</span>次下载</div><div class="list-data-box fl"><span class="list-data-num list-collection-num">'+sucList[i].collectionNum+'</span>次收藏</div></div><div class="list-data-price">售价：<span class="list-data-price-num">'+sucList[i].price+'</span>RMB</div><div class="list-data-update">发布时间：<span class="list-data-update-num">'+sucList[i].update+'</span></div></div><div class="designer-works-modify fl"><button class="works-modify-btn ">编辑</button><button class="works-cancel-btn">取消发布</button><input type="checkbox" class="works-cancel-check"/></div></div>'
				}
				sucStr+='<div class="designer-works-canelAll"><button class="works-canelAll-btn">批量取消发布</button><label for="checkall">全选</label><input type="checkbox" class="works-cancel-allcheck" id="checkall"/></div>';
			}else{
				sucStr='信息加载失败..';
			}
				designer_works_lists.append(sucStr);
		});

	});

	works_not_btn.on('click',funtion(){//未通过页面
		designer_works_lists.empty();
		var notStr ='';
		$.post('designer/photo_not_passed', {"page":1}, function(e){
			if(e){
				var notList = JSON.parse(e).list;
				for(var i=0,len=notList.length;i<len;i++){
				notStr+='</div><div class="designer-works-list-box clearfix"><div class="designer-works-list-bigpic fl"><img src="'+notList[i].bigPic+'" /></div><div class="designer-works-list-smdetail fl"><p class="designer-works-list-title">'+notList[i].name+'</p><p class="designer-works-list-describe">'+notList[i].describe+'</p><div class="designer-works-list-pics clearfix">';
					for(var j=0,jlen=notList[i].pic.length;j<jlen;j++){
						notList +='<img src="'+notList.pic[j]+'"/>';
					}
					notList+='</div></div><div class="designer-works-list-data fl"><div class="works-not-container clearfix"><p class="works-not-explain"><span>未通过说明:</span>'+notList[i].explain+'</p><p class="works-not-time fr">'+notList[i].notTime+'</p></div></div><div class="designer-works-modify fl"><button class="works-modify-btn ">编辑</button><button class="works-cancel-btn">取消发布</button><input type="checkbox" class="works-cancel-check"/></div></div>';
				}
			}else{
				notStr='信息加载失败';
			}
			designer_works_lists.append(notStr);
		});
	});

});