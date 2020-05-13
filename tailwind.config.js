module.exports = {
  theme: {
    extend: {
      colors: {
        brand: {
          blacklight: "#231F20",
          blackdark: "#191616",
          red: "#ec2726",
          indicator: "#C4C4C4",
        }
      },
      textColor: {
        brand: {
          white: "#DFDFDF",
          red: "#ec2726"
        }
      },
      fontSize: {
        "11": "11px",
        "12": "12px",
        "4.5xl": "2.5rem",
        "5mxl": "3.5rem",
        "8xl": "6rem",
        "10xl": "8rem",
      },
      fontFamily: {
        oswald: ["Oswald"],
        arvo: ["Arvo"]
      },
      height:{
      //px
      "18": "4.5rem",
      50: "50px",
      "148": "148px",
      "100": "100px",

      //vh
      "11vh": "11vh",
      "60vh": "60vh",
      "90vh": "90vh",

      // vw
      "6vw": "6vw",
      "35vw": "35vw",
      "40vw": "40vw",
      "45vw": "45vw",
      "50vw": "50vw",
      "60vw": "60vw",
      "62vw": "62vw",

      // percentage
      "35p": "35%",
      "40p": "40%",
      "60p": "60%",
      "80p": "80%",
      "90p": "90%",
      "95p": "95%",
      },
      minHeight: {
        50: "3.125rem",
        400: "25rem",
        675: "675px"
      },
      maxHeight: {
      //px
      24: "1.5rem",
      100: "6.25rem",
      125: "7.813rem",
      },
      width: {
        120: "120px",
        150: "150px",
        220: "220px",
        240: "240px",


        "7vw": "7vw",
        "8vw": "8vw",
        "9vw": "9vw",
        "50vw": "50vw",

        "90p": "90%",
      },
      minWidth: {
        65: "4.063rem",
        75: "75px",
        80: "80px",
        150: "150px",
        275: "17.19rem",
        280: "280px",
        300: "300px",
        320: "320px"
      },
      maxWidth: {
        200: "200px",
        300: "300px",
        350: "350px",
        370: "370px",
        450: "450px",
        524: "524px",
        769: "769px",
      },
      placeholderColor: {
        brand: {
          white: "#DFDFDF"
        }
      },
      opacity: {
        35: "0.35",
        60: "0.6",
        90: "0.9",
      },
      spacing: {
        "5vw": "5vw",
      },
      inset: {
      "89vh": "89vh",
      },
      borderRadius: {
        "2lg": "1rem",
        "3lg": "1.5rem",
        xl: "2.5rem",
        "2xl": "3.5rem",
      },
      borderColor: {
        brand: {
            red: "#ec2726"
        }
      },
      borderWidth: {
        3: "3px",
      },
      screens: {
        "2xl": "2048px",
        "3xl": "2560px"
      },
    }
  },
  variants: { width: ["responsive", "hover", "focus"] },
  plugins: []
};
