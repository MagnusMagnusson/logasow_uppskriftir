function setupFilters(){
    $("#flokkar input").on('input', e => {
        console.log('selected');
        const data = e.target.value;
        function getSelectedCategories(){
            return $("#flokkar input:checkbox:checked").map(function(){ return this.value; }).get();
        }

        function fetchFiltered(categories, query = ""){
            // Sends categories as repeated query params: ?flokkar=cat1&flokkar=cat2
            return $.ajax({
                url: '/u/api/filter/',
                method: 'GET',
                dataType: 'json',
                data: { flokkar: categories, q : query },
                traditional: true
            }).then(function(response){
                if(response.results){
                    return response.results;
                }
            }, function(err){
                console.error('Filter API error', err);
                return [];
            });
        }

        const debouncedFetch = (function(){
            let timer = null;
            return function(categories, query){
                return new Promise(resolve => {
                    clearTimeout(timer);
                    timer = setTimeout(() => {
                        fetchFiltered(categories, query).then(resolve);
                    }, 150);
                });
            };
        })();

        const applyFilter = (ids) => {
            if(ids.length === 0){
                $(`#uppskriftir li`).show();
                return;
            }
                
            $("#uppskriftir li").hide();
            for(let id of ids){
                $(`#uppskriftir li[data-id="${id}"]`).show();
            }
            $(".flokk-container").show();
            let lists = $("#uppskriftir ul");
            for(let list of lists){
                if($(list).children(':visible').length == 0){
                    $(list).parent().hide();
                }
            }
        }

        const selected = getSelectedCategories();
        const query = $("#searchbar").val();
        debouncedFetch(selected, query).then(results => {
            let ids = results.map(x => x.id);
            applyFilter(ids);
        });
    })
}

function setupRandomSelect(){
    var target = null;
    function pickRandom(iterations){
        console.log("pickrandom", iterations);
        if(iterations <= 0){
            setTimeout(() => {
                let href = $(target).attr('href');
                window.location.href = href;
            }, 1000);
            return;
        }
        let visible = $(".flokk-container li a:visible").not(".highlight");
        $(".highlight").removeClass("highlight");
        
        if(visible.length > 0){
            if(!target && visible.length === 1){
                return;
            }
            target = visible[Math.floor(Math.random() * visible.length)];
            $(target).addClass("highlight");
            setTimeout(() => {
                pickRandom(iterations - 1);
            }, 1500 / 7);
        }
    }
    $("#random-pick").on('click touchstart', e => {
        if(!target){
            pickRandom(7);
        }
    })
}

$(document).ready(e => {
    setupFilters();
    setupRandomSelect();
});
