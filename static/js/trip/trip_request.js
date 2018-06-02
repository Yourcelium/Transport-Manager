new Vue({
    el: '#ride-form',
    delimiters: ["[[", "]]"],
    data: {
        resident_select: true,
        first_name: "Test",
        last_name: "Test",
        DOB: "01/01/1111",
        resident_found: false,
        resident: null,
        procedure: "",
        
        destination: "",
        destination_list: null,
        destination_selected: false,
        search: "",
        new_destination: false,
        new_destination_name: "Test",
        new_destination_address: "Test",
        new_destination_suit: "1",
        new_destination_strecher: false,

        
        appointment_date: null,
        appointment_time: null,
        strecher: false,
        wheelchair: false,
        oxygen: false,
        oxygen_liters: 0,
        arranged_by: null,
        error : false,
        error_message: "",

        trip_completed: false,
        
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
            $.get("/schedule/resident/search/" + "?first_name=" + self.first_name + "&lastname=" + self.last_name + "&DOB=" + self.DOB)
            .done(function(resident){
                self.error = false
                self.resident = resident 
                self.resident_found = true
                self.resident_select = false
                console.dir(resident)    
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
                console.log(self.destination_list)
            })
        },
        findBy: function (list, value, column) {
            return list.filter(function (item) {
                return item[column].includes(value)
            })
        },
        newDestination: function(){
            this.new_destination = true
        },
        createDestination: function(){
            var self=this
            var csrf = $("#_true_csrf").val()
            console.log(csrf)
            // $.post( "/schedule/destination/create", { name: self.new_destination_name, address: self.new_destination_address, suit: self.new_destination_suit, strecher: self.new_destination_strecher, csrftoken: csrf } )

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
            })
            // $.post("/schedule/destination/create?name=" + self.new_destination_name + "&address=" + self.new_destination_address + "&suit=" + self.new_destination_suit + "&strecher=" + self.new_destination_suit)

        },
        selectDestination: function(event) {
            self = this
            var destination_id = event.target.attributes["data-id"]["value"]
            console.log(destination_id)
            $.get("/schedule/destination/get/?id=" + destination_id)
            .done(function(destination){
                self.destination = destination
                self.destination_selected = true
                console.log(self.destination)
                console.log(self.destination_selected)
                
            })
        },
        finishTrip: function() {

        } 
    },
    created: function(){
        this.getDestinations()
    },
    
    
})

