$(function() {//导航切换效果
	var navlist = $('.mainbody-nav-ul');

		navlist.each(function(index, el) {
			var navlist = $(this).find('li');
			navlist.each(function(index, el) {
				$(this).on('click',function(e){
					var _this = $(this),
						thisParent = _this.parent('ul'),
						thisShowlist = _this.parent().parent().siblings('.mainbody-list'),
						thisType = thisParent.siblings('h2').text(),
						thisStyle = _this.text();
						console.log(thisType+'  '+thisStyle);
					thisParent.children('li').removeClass('mainbody-nav-current');
					var thisleft = 105*(index%5);
					thisParent.find('span').animate({'left':thisleft}, 400);
					_this.addClass('mainbody-nav-current');
					thisShowlist.empty();
					$.post('/shop/filter-type',{ 'type': thisType,'style': thisStyle},function(data){
						var list = JSON.parse(data);
						var listStr;
						console.log(list);
						for(var i = 0,len=list.length;i<len;i++){

							//listStr += '<div class="list-goodsbox fl"><div class="list-picbox"><a href="#"><img src="'+list[i].preview_1 +'"alt="商品图片"/></a><div class="list-goods-name f14"><span class="fl">'+list[i].name+'</span><em class="fr"></em></div></div><p class="list-goods-describe f12">'+list[i].discription +'</p><div class="list-goods-show clearfix"><img src="'+list[i].preview_1+'" alt="商品图片" class="fl"/><img src="'+list[i].preview_2+'" alt="商品图片" class="fl"/><img src="'+list[i].preview_3+' " alt="商品图片" class="fl"/></div><div class=" list-goods-info f16 clearfix"><span class="list-goods-price fl">￥'+list[i].price+'</span><span class="list-goods-author fr">'+list[i].designer_name+'</span></div></div>'
						}
						thisShowlist.append(listStr);
				});
			});
		});
						
	});
});