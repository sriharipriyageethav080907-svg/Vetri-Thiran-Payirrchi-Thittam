async function api(url, options = {}) {

  const res = await fetch(
    url,
    {
      credentials: "include",
      ...options
    }
  );

  let data = {};

  try {
    data = await res.json();
  } catch {}

  if (!res.ok) {
    throw new Error(
      data.detail ||
      "Request failed"
    );
  }

  return data;
}


function setMessage(
  text,
  isError = true
) {

  const el =
    document.getElementById(
      "formMessage"
    );

  if (!el) return;

  el.textContent = text;

  el.style.color =
    isError
      ? "#b42318"
      : "#067647";
}


function money(
  n,
  currency = "INR"
) {

  try {

    return new Intl.NumberFormat(
      "en-IN",
      {
        style: "currency",
        currency
      }
    ).format(
      Number(n || 0)
    );

  } catch {

    return (
      `${currency} ` +
      Number(n || 0).toFixed(2)
    );
  }
}


function renderResult(r) {

  const box =
    document.getElementById(
      "results"
    );

  if (!box) return;


  const recs =
    (r.recommendations || [])
      .map(
        x => `
        <article class="rec">

          <small>
            ${x.category}
            ·
            ${x.platform}
          </small>

          <h3>
            ${escapeHtml(x.name)}
          </h3>

          <div class="price">

            ${money(
              x.estimated_price,
              x.currency
            )}

            × ${x.quantity}

          </div>

          <p>
            ${escapeHtml(
              x.description
            )}
          </p>

          <p>

            <strong>
              Why:
            </strong>

            ${escapeHtml(
              x.reason
            )}

          </p>

          ${
            x.search_url
              ? `
              <a
                href="${escapeAttr(
                  x.search_url
                )}"
                target="_blank"
                rel="noopener"
              >
                Search this option ↗
              </a>
              `
              : ""
          }

        </article>
        `
      )
      .join("");


  box.innerHTML = `

    <div class="result-head">

      <div>

        <p class="eyebrow">

          ${
            r.ai_generated
              ? "GEMINI AI"
              : "LOCAL FALLBACK"
          }

        </p>

        <h2>
          ${escapeHtml(
            r.title
          )}
        </h2>

      </div>

      <span class="badge">

        ${escapeHtml(
          r.budget_status
        )}

      </span>

    </div>


    <p class="summary">

      ${escapeHtml(
        r.summary
      )}

    </p>


    <div class="stats">

      <div class="stat">

        <small>
          Budget
        </small>

        <strong>

          ${money(
            r.budget,
            r.currency
          )}

        </strong>

      </div>


      <div class="stat">

        <small>
          Estimated total
        </small>

        <strong>

          ${money(
            r.estimated_total,
            r.currency
          )}

        </strong>

      </div>


      <div class="stat">

        <small>
          Saved plan
        </small>

        <strong>

          #${r.history_id || "—"}

        </strong>

      </div>

    </div>


    <h3>
      Recommendations
    </h3>


    <div class="rec-grid">

      ${
        recs ||
        "<p>No recommendations returned.</p>"
      }

    </div>


    <h3>
      Tips
    </h3>


    <ul>

      ${
        (r.tips || [])
          .map(
            t =>
              `<li>
                ${escapeHtml(t)}
              </li>`
          )
          .join("")
      }

    </ul>

  `;
}


function escapeHtml(v) {

  return String(
    v ?? ""
  ).replace(
    /[&<>"']/g,
    m => ({
      "&": "&amp;",
      "<": "&lt;",
      ">": "&gt;",
      '"': "&quot;",
      "'": "&#039;"
    }[m])
  );
}


function escapeAttr(v) {
  return escapeHtml(v);
}


const register =
  document.getElementById(
    "registerForm"
  );


if (register) {

  register.addEventListener(
    "submit",
    async e => {

      e.preventDefault();

      const f =
        new FormData(register);

      try {

        await api(
          "/register",
          {
            method: "POST",

            headers: {
              "Content-Type":
                "application/json"
            },

            body: JSON.stringify(
              Object.fromEntries(f)
            )
          }
        );

        setMessage(
          "Account created. Redirecting…",
          false
        );

        location.href =
          "/dashboard";

      } catch (err) {

        setMessage(
          err.message
        );

      }

    }
  );

}


const login =
  document.getElementById(
    "loginForm"
  );


if (login) {

  login.addEventListener(
    "submit",
    async e => {

      e.preventDefault();

      const f =
        new FormData(login);

      try {

        await api(
          "/login",
          {
            method: "POST",

            headers: {
              "Content-Type":
                "application/json"
            },

            body: JSON.stringify(
              Object.fromEntries(f)
            )
          }
        );

        setMessage(
          "Signed in. Redirecting…",
          false
        );

        location.href =
          "/dashboard";

      } catch (err) {

        setMessage(
          err.message
        );

      }

    }
  );

}


const plannerForm =
  document.getElementById(
    "plannerForm"
  );


if (plannerForm) {

  plannerForm.addEventListener(
    "submit",
    async e => {

      e.preventDefault();

      setMessage(
        "Generating plan…",
        false
      );

      const planner =
        plannerForm.dataset.planner;

      try {

        let body;

        let options = {
          method: "POST"
        };


        if (
          planner === "jewelry"
        ) {

          body =
            new FormData(
              plannerForm
            );

          options.body =
            body;

        } else {

          const f =
            new FormData(
              plannerForm
            );

          const raw =
            Object.fromEntries(f);

          let payload = {};


          if (
            planner === "home"
          ) {

            payload = {
              ...raw,

              budget:
                Number(
                  raw.budget
                ),

              rooms:
                raw.rooms
                  .split(",")
                  .map(
                    x => x.trim()
                  )
                  .filter(Boolean),

              preferred_platforms:
                raw.preferred_platforms
                  .split(",")
                  .map(
                    x => x.trim()
                  )
                  .filter(Boolean),

              items:
                raw.items
                  .split(",")
                  .map(
                    x => x.trim()
                  )
                  .filter(Boolean)
                  .map(
                    x => {

                      const [
                        name,
                        q
                      ] =
                        x.split(":");

                      return {
                        name:
                          name.trim(),

                        quantity:
                          Number(
                            q || 1
                          )
                      };

                    }
                  )
            };

          } else {

            payload = {
              ...raw,

              budget:
                Number(
                  raw.budget
                ),

              guests:
                Number(
                  raw.guests
                )
            };

          }


          options.headers = {
            "Content-Type":
              "application/json"
          };

          options.body =
            JSON.stringify(
              payload
            );

        }


        const result =
          await api(
            `/generate-${planner}`,
            options
          );


        setMessage(
          "Plan generated.",
          false
        );


        renderResult(
          result
        );


      } catch (err) {

        setMessage(
          err.message
        );

      }

    }
  );

}


const historyBox =
  document.getElementById(
    "history"
  );


if (historyBox) {

  (async () => {

    try {

      const rows =
        await api(
          "/history"
        );


      historyBox.innerHTML =
        rows.length

          ? rows
              .map(
                x => `

                <article class="panel">

                  <div class="result-head">

                    <div>

                      <span class="badge">

                        ${escapeHtml(
                          x.planner_type
                        )}

                      </span>

                      <h3>

                        ${escapeHtml(
                          x.result.title
                        )}

                      </h3>

                      <p>

                        ${escapeHtml(
                          x.result.summary
                        )}

                      </p>

                    </div>

                    <a
                      class="btn"
                      href="/recommendations-details/${x.id}"
                      target="_blank"
                    >
                      Open
                    </a>

                  </div>

                </article>

                `
              )
              .join("")

          : `

            <div class="panel">

              <p>
                No saved plans yet.
                Try a planner.
              </p>

            </div>

          `;


    } catch (err) {

      historyBox.innerHTML = `

        <div class="panel">

          <p>

            Please

            <a href="/login">
              sign in
            </a>

            to see your history.

          </p>

        </div>

      `;

    }

  })();

}
