
new Vue({
    el: '#trips-future',
    delimiters: ["[[", "]]"],
    data: {
        trips : [],
        days: 7,
        loading: false,
    },
    methods: {
        getFutureTrips: function(){
            this.loading=true;
            var self = this
            $.get('/schedule/trip/future' + '?days=' + self.days)
            .done(function(trips){
                self.trips = trips
                self.loading = false;
            })    
        },
        
        checkSubmit: function(event){
            if (event.code === 'Enter'){
                this.getFutureTrips()
            }
        }
        
    },
    created: function(){
        this.getFutureTrips()
    }
})