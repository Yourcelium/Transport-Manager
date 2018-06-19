Vue.component('date-picker', {
    template: '<input placeholder="Pick Date" />',
    props: [ 'dateFormat'],
    mounted: function() {
        var self = this;
        $(this.$el).datepicker({
            dateFormat: this.dateFormat,
            onSelect: function(trip_date) {
                self.$emit('update-date', trip_date)
            }
        });
    },
    beforeDestroy: function() {
        $(this.$el).datepicker('hide').datepicker('destory');
    }
});

new Vue({
    el: '#ride-form',
    delimiters: ["[[", "]]"],
    data: {
        request_in_progess: true,
        resident_form_display: true,
        first_name: "",
        last_name: "",
        DOB: "",
        
        resident: null,
        resident_chosen: false,
        procedure: "",
        
        destination_list_display: false,
        destination: "",
        destination_list: null,
        destination_selected: false,
        search: "",
        new_destination: false,
        new_destination_name: "",
        new_destination_address: "",
        new_destination_suit: "",
        new_destination_strecher: false,
        
        trip_date: '',
        trip_time: '',
        dateFormat: '',
        strecher: false,
        wheelchair: false,
        oxygen: false,
        oxygen_liters: 0,
        door_to_door: false,
        
        error : false,
        error_message: "",
        
        trip_completed: false,
        trip: null
        
    },
    computed: {
        destinationFilter: function() {
            return this.findBy(this.destination_list, this.search, 'address')
        }
    },
    methods: {
        searchResidents: function(){
            var self = this
            self.DOB = self.DOB.replace(/\/|_/g,'-');
            $.get("/schedule/resident/search/" + "?first_name=" + self.first_name + "&last_name=" + self.last_name + "&DOB=" + self.DOB)
            .done(function(resident){
                self.error = false
                self.resident = resident
                self.destination_list_display = true
                self.resident_form_display = false
                self.resident_chosen = true
            })
            .fail(function(data, textStatus, xhr) {
                self.error = true
                self.error_message = "Resident Not Found"
            })
        },
        checkSubmit: function(){
            this.searchResidents()        
        },
        getDestinations: function(){
            var self = this
            $.get("/schedule/destination/list")
            .done(function(destinations){
                self.destination_list = destinations
            })
        },
        findBy: function (list, value, column) {
            return list.filter(function (item) {
                return item[column].includes(value)
            })
        },
        newDestination: function(){
            this.new_destination = true
            this.destination_list_display = false
        },
        createDestination: function(){
            var self=this
            var csrf = $("#_true_csrf").val()
            $.ajax({
                url: '/schedule/destination/create',
                type: 'post',
                data: {
                    name: self.new_destination_name, 
                    address: self.new_destination_address, 
                    suit: self.new_destination_suit, 
                    strecher: self.new_destination_strecher
                },
                headers: {
                    "X-CSRFToken": csrf
                },
                dataType: 'json',
                success: function (data) {
                    console.info(data);
                }
            })
            .done(function(destination){
                self.destination = destination
                console.log(self.destination)
                self.new_destination=false
                self.destination_selected = true
            })
        },
        selectDestination: function(event) {
            var self = this
            var destination_id = event.target.attributes["data-id"]["value"]
            console.log(destination_id)
            $.get("/schedule/destination/get/?id=" + destination_id)
            .done(function(destination){
                self.destination = destination
                self.destination_list_display = false
                
            })
            self.destination_selected = true
            $( "#datepicker" ).datepicker(); 
        },
        finishTrip: function() {
            var self = this
            var appointment_datetime = this.trip_date + " " + this.trip_time
            console.log(this.trip_time)
            var csrf = $("#_true_csrf").val()            
            $.ajax({
                url: '/schedule/trip/request/create',
                type: 'post',
                data:{
                    resident : self.resident.id,
                    procedure : self.procedure,
                    destination : self.destination.id,
                    appointment_datetime : appointment_datetime,
                    strecher : self.strecher,
                    oxygen : self.oxygen,
                    oxygen_liters : self.oxygen_liters,
                    door_to_door : self.door_to_door
                    
                },
                headers: {
                    "X-CSRFToken": csrf
                },
                dataType: 'json'
            })
            .done(function(trip){
                self.trip = trip
                console.log(self.trip)
                self.destination_selected = false
                self.trip_completed = true
                self.request_in_progess = false
            })
            .fail(
                
            )
        },
        updateDate: function(trip_date) {
            this.trip_date = trip_date;
        }
        
    },
    created: function(){
        this.getDestinations()
        
        
    },
    
    
})

