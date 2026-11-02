import { FormEvent, useEffect, useState } from "react";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://127.0.0.1:8000";

type Metrics = {
  accuracy: number;
  precision_bad: number;
  recall_bad: number;
  f1_bad: number;
  roc_auc: number;
  confusion_matrix: number[][];
};

type ModelInfo = {
  model_type: string;
  target_label: string;
  dataset_status: string;
  metrics: Metrics;
  limitations: string[];
};

type Prediction = {
  predicted_class: "Good" | "Bad";
  probability_bad: number;
  probability_good: number;
  interpretation: string;
};

type FormState = {
  fruit: string;
  temp: string;
  humid: string;
  light: string;
  co2: string;
};

const initialForm: FormState = {
  fruit: "Orange",
  temp: "22",
  humid: "95",
  light: "7.36",
  co2: "361",
};

function formatPercent(value: number): string {
  return `${(value * 100).toFixed(2)}%`;
}

async function readApiError(response: Response): Promise<string> {
  try {
    const body = (await response.json()) as { detail?: string | Array<{ msg?: string }> };
    if (Array.isArray(body.detail)) return body.detail.map((item) => item.msg ?? "Invalid input").join(". ");
    return body.detail ?? "The request could not be completed.";
  } catch {
    return "The request could not be completed.";
  }
}

export default function App() {
  const [form, setForm] = useState<FormState>(initialForm);
  const [prediction, setPrediction] = useState<Prediction | null>(null);
  const [modelInfo, setModelInfo] = useState<ModelInfo | null>(null);
  const [modelInfoError, setModelInfoError] = useState<string | null>(null);
  const [requestError, setRequestError] = useState<string | null>(null);
  const [isPredicting, setIsPredicting] = useState(false);

  useEffect(() => {
    fetch(`${API_BASE_URL}/model-info`)
      .then(async (response) => {
        if (!response.ok) throw new Error(await readApiError(response));
        return response.json() as Promise<ModelInfo>;
      })
      .then(setModelInfo)
      .catch(() => setModelInfoError("Backend unavailable. Start the FastAPI server and refresh this page."));
  }, []);

  function updateField(field: keyof FormState, value: string) {
    setForm((current) => ({ ...current, [field]: value }));
  }

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setRequestError(null);
    setPrediction(null);
    setIsPredicting(true);
    try {
      const response = await fetch(`${API_BASE_URL}/predict`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          fruit: form.fruit,
          temp: Number(form.temp),
          humid: Number(form.humid),
          light: Number(form.light),
          co2: Number(form.co2),
        }),
      });
      if (!response.ok) throw new Error(await readApiError(response));
      setPrediction((await response.json()) as Prediction);
    } catch (error) {
      setRequestError(error instanceof Error ? error.message : "Backend unavailable. Check that the API is running.");
    } finally {
      setIsPredicting(false);
    }
  }

  const metrics = modelInfo?.metrics;

  return (
    <main className="min-h-screen bg-slate-50 text-slate-900">
      <div className="mx-auto max-w-6xl px-5 py-10 sm:px-8">
        <header className="mb-8 border-b border-slate-200 pb-7">
          <p className="mb-3 text-sm font-semibold uppercase tracking-[0.18em] text-blue-700">NNDL Review Demo</p>
          <h1 className="text-3xl font-bold tracking-tight text-slate-950 sm:text-4xl">Food Spoilage Risk Prediction</h1>
          <p className="mt-3 max-w-3xl text-base leading-7 text-slate-600">
            A neural-network demo for classifying the dataset&apos;s Good/Bad storage-condition label from fruit type and environmental readings.
          </p>
        </header>

        <section className="mb-8 rounded-xl border border-amber-200 bg-amber-50 px-5 py-4 text-sm leading-6 text-amber-950">
          <strong>Scope disclaimer.</strong> This demo does not forecast future spoilage and does not assess food safety or food freshness. It uses a provisional secondary dataset copy and reports a storage-condition classification only.
        </section>

        <div className="grid gap-7 lg:grid-cols-[1.05fr_0.95fr]">
          <section className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
            <h2 className="text-xl font-semibold">Manual prediction</h2>
            <p className="mt-1 text-sm text-slate-600">Enter environmental readings to run the saved Phase 2 model.</p>
            <form className="mt-6 grid gap-4 sm:grid-cols-2" onSubmit={submit}>
              <label className="field sm:col-span-2">
                <span>Fruit type</span>
                <select value={form.fruit} onChange={(event) => updateField("fruit", event.target.value)}>
                  {['Orange', 'Pineapple', 'Banana', 'Tomato'].map((fruit) => <option key={fruit}>{fruit}</option>)}
                </select>
              </label>
              <label className="field"><span>Temperature (°C)</span><input required type="number" step="any" value={form.temp} onChange={(event) => updateField("temp", event.target.value)} /></label>
              <label className="field"><span>Humidity (%)</span><input required type="number" min="0" max="100" step="any" value={form.humid} onChange={(event) => updateField("humid", event.target.value)} /></label>
              <label className="field"><span>Light intensity (Lux)</span><input required type="number" min="0" step="any" value={form.light} onChange={(event) => updateField("light", event.target.value)} /></label>
              <label className="field"><span>CO2 concentration (ppm)</span><input required type="number" min="0" step="any" value={form.co2} onChange={(event) => updateField("co2", event.target.value)} /></label>
              <button className="mt-2 rounded-lg bg-blue-700 px-5 py-3 text-sm font-semibold text-white transition hover:bg-blue-800 disabled:cursor-not-allowed disabled:bg-slate-400 sm:col-span-2" disabled={isPredicting} type="submit">
                {isPredicting ? "Running model…" : "Predict storage condition"}
              </button>
            </form>
            {requestError && <p role="alert" className="mt-4 rounded-lg bg-red-50 p-3 text-sm text-red-800">{requestError}</p>}
          </section>

          <section className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm" aria-live="polite">
            <h2 className="text-xl font-semibold">Prediction result</h2>
            {!prediction && <p className="mt-5 text-sm leading-6 text-slate-500">Submit the form to display the predicted storage-condition class and model probability.</p>}
            {prediction && (
              <div className="mt-5">
                <div className={`inline-flex rounded-full px-3 py-1 text-sm font-bold ${prediction.predicted_class === "Good" ? "bg-emerald-100 text-emerald-800" : "bg-red-100 text-red-800"}`}>
                  {prediction.predicted_class} storage-condition label
                </div>
                <dl className="mt-5 grid grid-cols-2 gap-4">
                  <div className="metric"><dt>Bad-label probability</dt><dd>{formatPercent(prediction.probability_bad)}</dd></div>
                  <div className="metric"><dt>Good-label probability</dt><dd>{formatPercent(prediction.probability_good)}</dd></div>
                </dl>
                <p className="mt-5 border-l-4 border-blue-600 pl-4 text-sm leading-6 text-slate-700">{prediction.interpretation}</p>
              </div>
            )}
          </section>
        </div>

        <section className="mt-8 rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
          <div className="flex flex-wrap items-start justify-between gap-3">
            <div><h2 className="text-xl font-semibold">Phase 2 model performance</h2><p className="mt-1 text-sm text-slate-600">Held-out test metrics from the saved model metadata.</p></div>
            {modelInfoError && <p role="alert" className="text-sm font-medium text-red-700">{modelInfoError}</p>}
          </div>
          {metrics && (
            <>
              <div className="mt-6 grid gap-3 sm:grid-cols-2 lg:grid-cols-5">
                {[
                  ["Accuracy", metrics.accuracy], ["Precision, Bad", metrics.precision_bad], ["Recall, Bad", metrics.recall_bad], ["F1, Bad", metrics.f1_bad], ["ROC-AUC", metrics.roc_auc],
                ].map(([label, value]) => <div className="metric" key={String(label)}><dt>{label}</dt><dd>{formatPercent(Number(value))}</dd></div>)}
              </div>
              <div className="mt-7 max-w-sm"><h3 className="text-sm font-semibold text-slate-800">Confusion matrix</h3><p className="mt-1 text-xs text-slate-500">Rows: actual. Columns: predicted. Order: Good, Bad.</p><div className="mt-3 grid grid-cols-3 overflow-hidden rounded-lg border border-slate-200 text-center text-sm"><div className="matrix-head"></div><div className="matrix-head">Good</div><div className="matrix-head">Bad</div><div className="matrix-head">Good</div><div className="matrix-cell">{metrics.confusion_matrix[0][0]}</div><div className="matrix-cell">{metrics.confusion_matrix[0][1]}</div><div className="matrix-head">Bad</div><div className="matrix-cell">{metrics.confusion_matrix[1][0]}</div><div className="matrix-cell">{metrics.confusion_matrix[1][1]}</div></div></div>
            </>
          )}
          {modelInfo && <p className="mt-7 text-xs leading-5 text-slate-500">Dataset status: {modelInfo.dataset_status}</p>}
        </section>
      </div>
    </main>
  );
}
