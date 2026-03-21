export default function parseErrors(error) {
  if (!error) return {};

  if (error.response && error.response.data) {
    const data = error.response.data;

    if (data.errors) {
      return data.errors;
    }

    if (data.error) {
      return { general: [data.error] };
    }

    return data;
  }

  return { general: ["Something went wrong"] };
}