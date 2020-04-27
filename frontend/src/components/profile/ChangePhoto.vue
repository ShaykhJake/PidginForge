<template>
  <v-row justify="center" class="ma-0">
    <v-dialog
      v-model="changePhotoDialog"
      scrollable
      persistent
      max-width="600px"
    >
      <template v-slot:activator="{ on: changePhotoDialog }">
        <v-tooltip bottom>
          <template v-slot:activator="{ on: tooltip }">
            <v-btn
              small
              fab
              class="orange lighten-4"
              v-on="{ ...tooltip, ...changePhotoDialog }"
            >
              <v-icon>edit</v-icon>
            </v-btn>
          </template>
          <span>Change Photo</span>
        </v-tooltip>
      </template>
      <v-card class="ma-0">
        <v-card-title class="pb-1 grey darken-4 white--text">
          Change Photo
        </v-card-title>
        
        <v-card-text class="pa-1 grey lighten-4">
          <v-container class="pa-1" fluid grid-list-md>
            <v-row wrap dense>
              <v-col cols="12">
                <v-file-input
                  :rules="rules"
                  show-size
                  @change="setImage"
                  accept="image/png, image/jpeg, image/gif"
                  placeholder="Pick a profile image"
                  prepend-icon="mdi-camera"
                  label="Profile Image"
                  ref="input"
                  name="image"
                ></v-file-input>
              </v-col>
            </v-row>

            <v-row wrap dense justify="center">
              <v-col cols="12">
                <section class="cropper-area">
                  <p class="text-center">Original</p>
                  <vue-cropper
                    ref="cropper"
                    :aspect-ratio="1"
                    :src="imageSource"
                    preview=".preview"
                    :auto-crop-area="1"
                  />
                </section>
              </v-col>
            </v-row>

            <v-row justify="center">
              <v-col cols="11">
                <div>
                  <v-spacer></v-spacer>
                  <v-btn @click.prevent="rotate(90)" class="mx-1">
                    <span class="hidden-sm-and-down">Rotate Right</span>
                    <v-icon>rotate_right</v-icon>
                  </v-btn>
                  <v-btn @click.prevent="rotate(-90)" class="mx-1">
                    <span class="hidden-sm-and-down">Rotate Left</span>
                    <v-icon>rotate_left</v-icon>
                  </v-btn>
                  <v-btn @click.prevent="rotate(90)" class="mx-1">
                    <span class="hidden-sm-and-down">Flip Image</span>
                    <v-icon>flip</v-icon>
                  </v-btn>
                </div>
              </v-col>
            </v-row>
            <v-row>
              <v-spacer></v-spacer>
              <v-col cols="7" md="3">
                <p class="text-center">Avatar Preview</p>
                <div class="preview avatar text-center" />
              </v-col>
              <v-spacer></v-spacer>
            </v-row>

            <v-row>
              <v-col cols="12">
                <div class="content"></div>
              </v-col>
            </v-row>
          </v-container>
        </v-card-text>
        <v-card-actions class="grey darken-4 white--text">
          <v-spacer></v-spacer>
          <v-btn
            color="orange lighten-2"
            @click="cancelDialog"
            :hidden="success"
            ><v-icon>cancel</v-icon>Cancel</v-btn
          >
          <!-- <v-btn 
            color="orange lighten-2" 
            @click="checkPhoto"
            :disabled="!valid"
          >Check If Available</v-btn> -->
          <v-btn v-if="!success"
            color="blue lighten-2"
            @click="onSubmit"
            :loading="submitting"
            ><v-icon>done</v-icon>Submit</v-btn
          >
          <v-btn v-else color="blue lighten-2" @click="cancelDialog">
            ><v-icon>done_outline</v-icon>Close</v-btn
          >
          <v-spacer></v-spacer>
          <!-- TODO: need to ensure that the user information is reloaded after saving -->
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-row>
</template>
<script>
import VueCropper from "vue-cropperjs";
import "cropperjs/dist/cropper.min.css";
import { apiFileService } from "@/common/api.fileservice.js";

export default {
  name: "ChangePhoto",
  components: {
    VueCropper
  },
  props: {
    imgSrc: String,
    imgName: String
  },
  data() {
    return {
      imageSource: String,
      imageName: String,
      loadingImage: false,
      cropImg: "",
      data: null,
      cropper: {},
      destination: {},
      image: {},
      imageFile: [],
      selectedFile: null,
      confirmPhoto: "",
      valid: false,
      available: false,
      changePhotoDialog: false,
      error: null,
      success: false,
      thinking: false,
      changeSuccessMessage: "",
      changeerror: false,
      submitting: false,
      changeErrorMessage: "",
      rules: [
        value =>
          !value ||
          value.size < 500000 ||
          "Image size should be less than 500kb!"
      ],
      notification: {
        message: "",
        type: ""
      }
    };
  },
  methods: {
    initializeImage() {

      this.imageSource = this.imgSrc;
      this.imageName = this.imgName;
    },
    cropImage() {
      // get image data for post processing, e.g. upload or setting image src
      this.cropImg = this.$refs.cropper.getCroppedCanvas().toDataURL();
    },
    flipX() {
      const dom = this.$refs.flipX;
      let scale = dom.getAttribute("data-scale");
      scale = scale ? -scale : -1;
      this.$refs.cropper.scaleX(scale);
      dom.setAttribute("data-scale", scale);
    },
    flipY() {
      const dom = this.$refs.flipY;
      let scale = dom.getAttribute("data-scale");
      scale = scale ? -scale : -1;
      this.$refs.cropper.scaleY(scale);
      dom.setAttribute("data-scale", scale);
    },
    getCropBoxData() {
      this.data = JSON.stringify(this.$refs.cropper.getCropBoxData(), null, 4);
    },
    reset() {
      this.$refs.cropper.reset();
    },
    rotate(deg) {
      this.$refs.cropper.rotate(deg);
    },
    setCropBoxData() {
      if (!this.data) return;
      this.$refs.cropper.setCropBoxData(JSON.parse(this.data));
    },
    setImage(newimage) {
      this.loadingImage = true;
      this.imageName = newimage.name;
      const file = newimage;
      if (file.type.indexOf("image/") === -1) {
        alert("Please select an image file");
        return;
      }
      if (typeof FileReader === "function") {
        const reader = new FileReader();
        reader.onload = event => {
          this.imageSource = event.target.result;
          // rebuild cropperjs with the updated source
          this.$refs.cropper.replace(event.target.result);
        };
        reader.readAsDataURL(file);
        this.loadingImage = false;
      } else {
        console.log("Sorry, that file is not supported");
        this.loadingImage = false;
      }
    },
    onSubmit() {
      // The following grabs the blob, converts to a JPEG, wraps it, and sends it to the API
      this.submitting = true;
      const canvas = this.$refs.cropper.getCroppedCanvas();
      let stripped = this.imageName.split(".");
      let newfilename = stripped[0].concat(".jpg");
      canvas.toBlob(
        blob => {
          const formData = new FormData();
          formData.append("image", blob, newfilename);
          let endpoint = `/api/users/profileimageupload/`;
          apiFileService(endpoint, "PATCH", formData).then(data => {
            if (data.success === true) {
              this.error = false;
              this.success = true;
              this.changeSuccessMessage = data.message;
              // console.log(data.message);
              this.$emit("emitUserDataChange");
              this.submitting = false;
              this.cancelDialog();
            } else {
              this.changeerror = true;
              this.success = false;
              this.changeErrorMessage = data.message;
              // console.log(data.message);
            }
          });
        },
        "image/jpeg",
        0.85
      );
      this.reset();
    },
    closeDialog() {
      this.changePhotoDialog = false;
    },
    cancelDialog() {
      // this.$refs.form.reset();
      this.changePhotoDialog = false;
      this.error = false;
      this.success = false;
      this.available = false;
      this.reset();
    }
  },
  created() {
    this.initializeImage();
  }
};
</script>
<style scoped type="text/css">
body {
  margin: 0 auto;
}
input[type="file"] {
  display: none;
}
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 0 5px 0;
}
.header h2 {
  margin: 0;
}
.header a {
  text-decoration: none;
  color: black;
}
.content {
  display: flex;
  justify-content: space-between;
}
.cropper-area {
  width: 100%;
}
.actions {
  margin-top: 1rem;
}
.actions a {
  display: inline-block;
  padding: 3px 3px;
  background: #0062cc;
  color: white;
  text-decoration: none;
  border-radius: 3px;
  /* margin-right: 1rem; */
  /* margin-bottom: 1rem; */
}
textarea {
  width: 100%;
  height: 100px;
}
.preview-area {
  width: 100%;
}
.preview-area p {
  font-size: 1.25rem;
  margin: 0;
  margin-bottom: 1rem;
}
.preview-area p:last-of-type {
  margin-top: 1rem;
}
.preview {
  width: 100%;
  /* height: calc(372px * (9 / 16)); */
  height: 250px;
  overflow: hidden;
}
.avatar {
  width: 175px;
  /* height: calc(372px * (9 / 16)); */
  height: 175px;
  overflow: hidden;
  border-radius: 50%;
}
.img-container img {
  width: 100%;
}
.crop-placeholder {
  width: 100%;
  height: 200px;
  background: #ccc;
}
.cropped-image img {
  max-width: 100%;
}
</style>
