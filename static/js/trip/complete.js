new Vue({
    el: '#trip-complete',
    delimiters: ["[[", "]]"],
    data: {
        csrf: null,
        tripID: null,
        trip: null,
        transport_provider: '',
        pick_up_time: '',
        return_time: '',
        requestID: '',
        notes: '',
        error: false,
        error_message: ''
    },
    methods: {
        checkTime: function() {
            var self = this
            console.log(self.return_time)
            if (self.pick_up_time !== '' && self.return_time !== '') {
                var pick_up = Number(self.pick_up_time.replace(':', ''))
                var return_ = Number(self.return_time.replace(':', ''))
                console.log(pick_up, return_)
                if (pick_up > return_) {
                    self.error = true
                    self.error_message = "Pick Up Time Must Be Before Return Time"
                }
            }
        },
        finishTrip: function() {
            var self = this
            this.checkTime()
            if (self.error === false) {
                $.ajax({
                    url: '/schedule/trip/complete/' + self.tripID,
                    type: 'post',
                    data:{
                        transport_provider: self.transport_provider,
                        pick_up_time : self.pick_up_time,
                        return_time : self.return_time,
                        requestID: self.requestID,
                        notes: self.notes
                    },
                    headers: {
                        "X-CSRFToken": self.csrf
                    },
                    dataType: 'json'
                })
                .done(function(trip){
                    //window.close()
                })
            }
            
            
        },
        formatDate: function(date) {
            return moment(date).format('YYYY-MM-DD')
        }
    },
    mounted: function(){
        var self = this 
        self.csrf = $("#_true_csrf").val()
        self.tripID = $("#tripID").val()
        $.get("/schedule/trip/api/detail/" + self.tripID)
        .done(function(trip){
            self.trip = trip
        })
        console.log(self.tripID)
    }
})