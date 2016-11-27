(function (js) {

    const addBar = function (user) {
        console.log("bar added");
        js(document.body)
            .prepend(`
                <div id="hack-bar-button" class="hack-bar-button" >
                    <a href="http://hackhate.huguesverlin.fr/social_analysis?text=${user}" target="_blank">Analyse</a>
                </div>
                <script></script>
                `);
    };

    const url = window.location.href;
    let re = new RegExp(/facebook\.com\/(\w+)\//);
    let page = re.exec(url);
    if (page && page.length > 1) {
        let user = page[1];
        addBar(user)
    } else {
        re = new RegExp(/twitter\.com\/(\w+)/);
        let page = re.exec(url);
        if (page && page.length > 1) {
            addBar(page[1])
        }
    }

})(jQuery);





