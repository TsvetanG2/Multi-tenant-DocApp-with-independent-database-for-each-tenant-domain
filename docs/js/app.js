<script>
    $(document).ready(function() {
    $.ajax({
        url: '{% url "fetch_events" %}',
        dataType: 'json',
        success: function(data) {
            $('#calendar').fullCalendar({
                events: data
            });
        }
    });
});
</script>