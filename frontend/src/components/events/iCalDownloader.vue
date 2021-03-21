<template>
  <v-dialog v-model="showDialog" width="275" persistent scrollable>
    <v-card class="sandstone calligraphy--text">
      <v-card-title>
        Export Event(s)
      </v-card-title>
      <v-card-text class="desertsand calligraphy--text pa-2">
        Click on the Download button to generate a standard .ics calendar file
        for
        {{ exportList.length > 1 ? `${exportList.length} events` : "1 event" }}.
      </v-card-text>

      <v-card-actions class="sandstone">
        <v-btn @click="closeDialog" class="garbage desertsand--text"
          >Cancel<v-icon right>mdi-cancel</v-icon></v-btn
        >
        <v-spacer></v-spacer>
        <v-btn :loading="generatingFile" @click="contentWriter" class="primary"
          >Download<v-icon right>mdi-send</v-icon></v-btn
        >
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
<script>
export default {
  name: "iCalDownloader",
  components: {},
  fileContents: "",
  fileName: "",
  downloadLink: "",
  props: {
    exportList: Array,
    showDialog: Boolean
  },
  data: () => ({
    generatingFile: false
  }),
  computed: {},
  methods: {
    closeDialog() {
      this.$emit("closeDialog");
    },
    downloadFile(name, contents, mime_type) {
      mime_type = mime_type || "text/calendar";
      // mime_type = mime_type || "text/plain";
      var blob = new Blob([contents], { type: mime_type });

      var dlink = document.createElement("a");
      dlink.download = name;
      dlink.href = window.URL.createObjectURL(blob);
      dlink.onclick = function(e) {
        // revokeObjectURL needs a delay to work properly
        var that = this;
        setTimeout(function() {
          window.URL.revokeObjectURL(that.href);
        }, 1500);
        return e;
      };

      dlink.click();
      dlink.remove();
    },
    formatDate(date) {
      date = date.substring(0, 17);
      console.log(date);
      date = date.replace(/-/g, "");
      date = date.replace(/:/g, "");
      date += "00Z";
      console.log(date);
      return date;
    },
    contentWriter() {
      if (!this.exportList) {
        return false;
      }
      var fileContent =
        "BEGIN:VCALENDAR\n" +
        "VERSION:2.0\n" +
        "CALSCALE:GREGORIAN\n" +
        "PRODID:-//PidginForge.org//Events Calendar//EN\n" +
        "METHOD:PUBLISH\n";
      for (var item of this.exportList) {
        fileContent +=
          "BEGIN:VEVENT\n" +
          `SUMMARY:${item.name}\n` +
          `UID:${item.uid}` +
          "SEQUENCE:0\n" +
          "STATUS:CONFIRMED\n" +
          "TRANSP:TRANSPARENT\n" +
          // 'RRULE:FREQ=YEARLY;INTERVAL=1;BYMONTH=2;BYMONTHDAY=12\n' +
          `DTSTART:${this.formatDate(item.start_datetime)}\n` +
          `DTEND:${this.formatDate(item.end_datetime)}\n` +
          `DTSTAMP:${this.formatDate(item.curationdate)}\n` +
          // `DTSTAMP:${item.curationdate.replace('-', '')}}\n` +
          `CATEGORIES:${item.topic}\n` +
          `LOCATION:${item.location}\n` +
          "GEO:\n" +
          `DESCRIPTION:${item.caption}\n` +
          "URL:\n" +
          "END:VEVENT\n";
        console.log(item);
      }
      fileContent += `END:VCALENDAR`;
      if (this.exportList.length === 1) {
        var fileName = `${item.slug}.ics`;
      } else {
        var todayDate = new Date();
        fileName = `PF_EventsList_${todayDate.toLocaleDateString()}.ics`;
      }
      console.log(fileName, fileContent);
      this.downloadFile(fileName, fileContent);

      // var archiveSample =
      //   `BEGIN:VCALENDAR
      //   VERSION:2.0
      //   PRODID:-//ZContent.net//Zap Calendar 1.0//EN
      //   CALSCALE:GREGORIAN
      //   METHOD:PUBLISH
      //   BEGIN:VEVENT
      //   SUMMARY:Abraham Lincoln
      //   UID:c7614cff-3549-4a00-9152-d25cc1fe077d
      //   SEQUENCE:0
      //   STATUS:CONFIRMED
      //   TRANSP:TRANSPARENT
      //   RRULE:FREQ=YEARLY;INTERVAL=1;BYMONTH=2;BYMONTHDAY=12
      //   DTSTART:20080212
      //   DTEND:20080213
      //   DTSTAMP:20150421T141403
      //   CATEGORIES:U.S. Presidents,Civil War People
      //   LOCATION:Hodgenville\, Kentucky
      //   GEO:37.5739497;-85.7399606
      //   DESCRIPTION:Born February 12\, 1809\nSixteenth President (1861-1865)\n\n\n\nhttp://AmericanHistoryCalendar.com
      //   URL:http://americanhistorycalendar.com/peoplecalendar/1,328-abraham-lincoln
      //   END:VEVENT
      //   END:VCALENDAR`;
    }
  },

  mounted() {
    if (this.userRsvp) {
      this.RSVP = this.userRsvp;
    } else {
      this.RSVP = {};
    }
  }
};
</script>
<style lang="stylus"></style>
