function setupHandlers(){
    $("#flokkar input").on('input', e => {
        console.log('selected');
        const data = e.target.value;
        function getSelectedCategories(){
            return $("#flokkar input:checkbox:checked").map(function(){ return this.value; }).get();
        }

        function fetchFiltered(categories){
            // Sends categories as repeated query params: ?flokkar=cat1&flokkar=cat2
            return $.ajax({
                url: '/u/api/filter/',
                method: 'GET',
                dataType: 'json',
                data: { flokkar: categories },
                traditional: true
            }).then(function(response){
                console.log("r", response);
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
            return function(categories){
                return new Promise(resolve => {
                    clearTimeout(timer);
                    timer = setTimeout(() => {
                        fetchFiltered(categories).then(resolve);
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
                console.log(id)
                $(`#uppskriftir li[data-id="${id}"]`).show();
            }
            $(".flokk-container").show();
            let lists = $("#uppskriftir ul");
            for(let list of lists){
                console.log(list);
                console.log($(list).children(':visible').length)
                if($(list).children(':visible').length == 0){
                    console.log("HIDE!");
                    console.log($(list).parent())
                    $(list).parent().hide();
                }
            }
        }

        // This is the code that runs when any checkbox changes (replace the placeholder)
        const selected = getSelectedCategories();
        debouncedFetch(selected).then(results => {
            let ids = results.map(x => x.id);
            applyFilter(ids);
        });
    })
}

$(document).ready(e => {
    console.log("Redz");
    setupHandlers();
});
