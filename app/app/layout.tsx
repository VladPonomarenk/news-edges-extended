
export const metadata = { title: "Global Shifts & Edges" };
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (<html lang="en"><body><div className="mx-auto max-w-6xl p-6">{children}</div>
    <style>{`*{box-sizing:border-box} body{font-family:ui-sans-serif,system-ui,Segoe UI,Roboto,Helvetica,Arial}
    .badge{display:inline-flex;align-items:center;border:1px solid #e5e7eb;border-radius:9999px;padding:2px 8px;font-size:12px}
    input,select{border:1px solid #e5e7eb;border-radius:12px;padding:8px 12px}
    a.card{border:1px solid #e5e7eb;border-radius:16px;padding:16px;display:block;text-decoration:none;color:inherit}
    a.card:hover{box-shadow:0 6px 24px rgba(0,0,0,0.06)}`}</style></body></html>);
}
