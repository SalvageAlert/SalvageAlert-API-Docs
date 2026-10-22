// Free call: your plan, balance and rate limit. Node 18+.
const res = await fetch('https://salvagealert.com/api/v1/me', {
  headers: { Authorization: `Bearer ${process.env.SALVAGEALERT_KEY}` },
});
console.log(res.status, await res.json());
