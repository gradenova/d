
function SEARCH_ENGINE(dom,searchInput,searchResultInner,searchList,searchItemID){

    //存储拼音+汉字+数字的数组
    this.searchMemberArray = [];

    //存储搜索结果的ID(待扩展)
    this.searchResultID = [];

    //作用对象
    this.dom = $("." + dom);

    //搜索框
    this.searchInput = "." + searchInput;

    //搜索结果框
    this.searchResultInner = this.dom.find("." + searchResultInner);

    //搜索对象的名单列表
    this.searchList = this.dom.find("." + searchList);

    //存储搜索项目的ID，便于搜索结果的显示，是个数组
    this.searchItemIDArray = this.dom.find("." + searchItemID);

    //转换成拼音并存入数组
    this.transformPinYin();

    //绑定搜索事件
    this.searchActiveEvent();

}

SEARCH_ENGINE.prototype = {
    //-----------------------------【转换成拼音，并将拼音、汉字、数字存入数组】
    transformPinYin : function(){

        //临时存放数据对象
        $("body").append('<input type="text" class="hidden pingying-box">');
        var $pinyin = $("input.pingying-box");

        for(var i=0;i<this.searchList.length;i++){

            //存放名字，转换成拼音
            $pinyin.val(this.searchList.eq(i).val());

            //汉字转换成拼音
            var pinyin = $pinyin.toPinyin().toLowerCase().replace(/\s/g,"");

            //汉字
            var cnCharacter = this.searchList.eq(i).val();

            //ID
            var itemID = this.searchItemIDArray.eq(i).attr("id");

            //数字
            var digital = this.searchList.eq(i).val().replace(/[^0-9]/ig,"");

            //存入数组
            this.searchMemberArray.push(pinyin + "&" + cnCharacter + "&" + digital + "&" + itemID);
        }

        //删除临时存放数据对象
        $pinyin.remove();
    },

    //-----------------------------【模糊搜索关键字】
    fuzzySearch : function(type,val){
        var s;
        var returnArray = [];

        //拼音
        if(type === "pinyin"){
            s = 0;
        }
        //汉字
        else if(type === "cnCharacter"){
            s = 1;
        }
        //数字
        else if(type === "digital"){
            s = 2;
        }

        for(var i=0;i<this.searchMemberArray.length;i++){
            //包含字符
            if(this.searchMemberArray[i].split("&")[s].indexOf(val) >= 0){
                returnArray.push(this.searchMemberArray[i]);
            }
        }

        return returnArray;

    },

    //-----------------------------【输出搜索结果】
    postMemberList : function(tempArray){
        var html = '';

        //有搜索结果
        if(tempArray.length > 0){

            $('.search-item-list').children().hide();
            for(var i=0;i<tempArray.length;i++){
                var sArray = tempArray[i].split("&");           
                $('#' + sArray[3] + '').show();
            }
        }
        //无搜索结果
        else{
            if($(this.searchInput).val() == ""){
                $('.search-item-list > [date-page='+vm_pagination.presentPage+']').show();
            }
            else{
                $('.search-item-list').children().hide();
            }
        }
    },

    //-----------------------------【绑定搜索事件】
    searchActiveEvent : function(){

        var searchEngine = this;

        $(document).on("keyup",this.searchInput,function(){

            //临时存放找到的数组
            var tempArray = [];

            var val = $(this).val();

            //判断拼音的正则
            var pinYinRule = /^[A-Za-z]+$/;

            //判断汉字的正则
            var cnCharacterRule = new RegExp("^[\\u4E00-\\u9FFF]+$","g");

            //判断整数的正则
            var digitalRule = /^[-\+]?\d+(\.\d+)?$/;

            //只搜索3种情况
            //拼音
            if(pinYinRule.test(val)){
                tempArray = searchEngine.fuzzySearch("pinyin",val);
            }
            //汉字
            else if(cnCharacterRule.test(val)){
                tempArray = searchEngine.fuzzySearch("cnCharacter",val);
            }
            //数字
            else if(digitalRule.test(val)){
                tempArray = searchEngine.fuzzySearch("digital",val);
            }
            else{
                $('.search-item-list > [date-page!='+vm_pagination.presentPage+']').hide();
                $('.search-item-list > [date-page='+vm_pagination.presentPage+']').show();
                //$('.search-item-list').children().show();
            }

            searchEngine.postMemberList(tempArray);

        });
    }
};




function SEARCH_ENGINE1(dom,searchInput,searchResultInner,searchList,searchItemID){

    //存储拼音+汉字+数字的数组
    this.searchMemberArray = [];

    //存储搜索结果的ID(待扩展)
    this.searchResultID = [];

    //作用对象
    this.dom = $("." + dom);

    //搜索框
    this.searchInput = "." + searchInput;

    //搜索结果框
    this.searchResultInner = this.dom.find("." + searchResultInner);

    //搜索对象的名单列表
    this.searchList = this.dom.find("." + searchList);

    //存储搜索项目的ID，便于搜索结果的显示，是个数组
    this.searchItemIDArray = this.dom.find("." + searchItemID);

    //转换成拼音并存入数组
    this.transformPinYin();

    //绑定搜索事件
    this.searchActiveEvent();

}

SEARCH_ENGINE1.prototype = {
    //-----------------------------【转换成拼音，并将拼音、汉字、数字存入数组】
    transformPinYin : function(){

        //临时存放数据对象
        $("body").append('<input type="text" class="hidden pingying-box">');
        var $pinyin = $("input.pingying-box");

        for(var i=0;i<this.searchList.length;i++){

            //存放名字，转换成拼音
            $pinyin.val(this.searchList.eq(i).val());

            //汉字转换成拼音
            var pinyin = $pinyin.toPinyin().toLowerCase().replace(/\s/g,"");

            //汉字
            var cnCharacter = this.searchList.eq(i).val();

            //ID
            var itemID = this.searchItemIDArray.eq(i).attr("id");

            //数字
            var digital = this.searchList.eq(i).val().replace(/[^0-9]/ig,"");

            //存入数组
            this.searchMemberArray.push(pinyin + "&" + cnCharacter + "&" + digital + "&" + itemID);
        }

        //删除临时存放数据对象
        $pinyin.remove();
    },

    //-----------------------------【模糊搜索关键字】
    fuzzySearch : function(type,val){
        var s;
        var returnArray = [];

        //拼音
        if(type === "pinyin"){
            s = 0;
        }
        //汉字
        else if(type === "cnCharacter"){
            s = 1;
        }
        //数字
        else if(type === "digital"){
            s = 2;
        }

        for(var i=0;i<this.searchMemberArray.length;i++){
            //包含字符
            if(this.searchMemberArray[i].split("&")[s].indexOf(val) >= 0){
                returnArray.push(this.searchMemberArray[i]);
            }
        }

        return returnArray;

    },

    //-----------------------------【输出搜索结果】
    postMemberList : function(tempArray){
        var html = '';

        //有搜索结果
        if(tempArray.length > 0){

            $('.search-item-list1').children().hide();
            for(var i=0;i<tempArray.length;i++){
                var sArray = tempArray[i].split("&");           
                $('#' + sArray[3] + '').show();
            }
        }
        //无搜索结果
        else{
            if($(this.searchInput).val() == ""){
                $('.search-item-list1 > [date-page='+vm_pagination.presentPage1+']').show();
            }
            else{
                $('.search-item-list1').children().hide();
            }
        }
    },

    //-----------------------------【绑定搜索事件】
    searchActiveEvent : function(){

        var searchEngine = this;

        $(document).on("keyup",this.searchInput,function(){

            //临时存放找到的数组
            var tempArray = [];

            var val = $(this).val();

            //判断拼音的正则
            var pinYinRule = /^[A-Za-z]+$/;

            //判断汉字的正则
            var cnCharacterRule = new RegExp("^[\\u4E00-\\u9FFF]+$","g");

            //判断整数的正则
            var digitalRule = /^[-\+]?\d+(\.\d+)?$/;

            //只搜索3种情况
            //拼音
            if(pinYinRule.test(val)){
                tempArray = searchEngine.fuzzySearch("pinyin",val);
            }
            //汉字
            else if(cnCharacterRule.test(val)){
                tempArray = searchEngine.fuzzySearch("cnCharacter",val);
            }
            //数字
            else if(digitalRule.test(val)){
                tempArray = searchEngine.fuzzySearch("digital",val);
            }
            else{
                $('.search-item-list1 > [date-page!='+vm_pagination.presentPage1+']').hide();
                $('.search-item-list1 > [date-page='+vm_pagination.presentPage1+']').show();
                //$('.search-item-list').children().show();
            }

            searchEngine.postMemberList(tempArray);

        });
    }
};


function SEARCH_ENGINE2(dom,searchInput,searchResultInner,searchList,searchItemID){

    //存储拼音+汉字+数字的数组
    this.searchMemberArray = [];

    //存储搜索结果的ID(待扩展)
    this.searchResultID = [];

    //作用对象
    this.dom = $("." + dom);

    //搜索框
    this.searchInput = "." + searchInput;

    //搜索结果框
    this.searchResultInner = this.dom.find("." + searchResultInner);

    //搜索对象的名单列表
    this.searchList = this.dom.find("." + searchList);

    //存储搜索项目的ID，便于搜索结果的显示，是个数组
    this.searchItemIDArray = this.dom.find("." + searchItemID);

    //转换成拼音并存入数组
    this.transformPinYin();

    //绑定搜索事件
    this.searchActiveEvent();

}

SEARCH_ENGINE2.prototype = {
    //-----------------------------【转换成拼音，并将拼音、汉字、数字存入数组】
    transformPinYin : function(){

        //临时存放数据对象
        $("body").append('<input type="text" class="hidden pingying-box">');
        var $pinyin = $("input.pingying-box");

        for(var i=0;i<this.searchList.length;i++){

            //存放名字，转换成拼音
            $pinyin.val(this.searchList.eq(i).val());

            //汉字转换成拼音
            var pinyin = $pinyin.toPinyin().toLowerCase().replace(/\s/g,"");

            //汉字
            var cnCharacter = this.searchList.eq(i).val();

            //ID
            var itemID = this.searchItemIDArray.eq(i).attr("id");

            //数字
            var digital = this.searchList.eq(i).val().replace(/[^0-9]/ig,"");

            //存入数组
            this.searchMemberArray.push(pinyin + "&" + cnCharacter + "&" + digital + "&" + itemID);
        }

        //删除临时存放数据对象
        $pinyin.remove();
    },

    //-----------------------------【模糊搜索关键字】
    fuzzySearch : function(type,val){
        var s;
        var returnArray = [];

        //拼音
        if(type === "pinyin"){
            s = 0;
        }
        //汉字
        else if(type === "cnCharacter"){
            s = 1;
        }
        //数字
        else if(type === "digital"){
            s = 2;
        }

        for(var i=0;i<this.searchMemberArray.length;i++){
            //包含字符
            if(this.searchMemberArray[i].split("&")[s].indexOf(val) >= 0){
                returnArray.push(this.searchMemberArray[i]);
            }
        }

        return returnArray;

    },

    //-----------------------------【输出搜索结果】
    postMemberList : function(tempArray){
        var html = '';

        //有搜索结果
        if(tempArray.length > 0){

            $('.search-item-list2').children().hide();
            for(var i=0;i<tempArray.length;i++){
                var sArray = tempArray[i].split("&");           
                $('#' + sArray[3] + '').show();
            }
        }
        //无搜索结果
        else{
            if($(this.searchInput).val() == ""){
                $('.search-item-list2 > [date-page='+vm_pagination.presentPage2+']').show();
            }
            else{
                $('.search-item-list2').children().hide();
            }
        }
    },

    //-----------------------------【绑定搜索事件】
    searchActiveEvent : function(){

        var searchEngine = this;

        $(document).on("keyup",this.searchInput,function(){

            //临时存放找到的数组
            var tempArray = [];

            var val = $(this).val();

            //判断拼音的正则
            var pinYinRule = /^[A-Za-z]+$/;

            //判断汉字的正则
            var cnCharacterRule = new RegExp("^[\\u4E00-\\u9FFF]+$","g");

            //判断整数的正则
            var digitalRule = /^[-\+]?\d+(\.\d+)?$/;

            //只搜索3种情况
            //拼音
            if(pinYinRule.test(val)){
                tempArray = searchEngine.fuzzySearch("pinyin",val);
            }
            //汉字
            else if(cnCharacterRule.test(val)){
                tempArray = searchEngine.fuzzySearch("cnCharacter",val);
            }
            //数字
            else if(digitalRule.test(val)){
                tempArray = searchEngine.fuzzySearch("digital",val);
            }
            else{
                $('.search-item-list2 > [date-page!='+vm_pagination.presentPage2+']').hide();
                $('.search-item-list2 > [date-page='+vm_pagination.presentPage2+']').show();
                //$('.search-item-list').children().show();
            }

            searchEngine.postMemberList(tempArray);

        });
    }
};