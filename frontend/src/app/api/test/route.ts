import { NextRequest, NextResponse } from "next/server";

export async function GET(req: NextRequest) {
  try {
    // Test the backend connection
    const res = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000"}/health`);

    if (!res.ok) {
      return NextResponse.json(
        { error: "Could not reach backend", backendStatus: res.status },
        { status: 503 }
      );
    }

    const backendData = await res.json();

    return NextResponse.json({
      frontend: "OK",
      backend: backendData,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    console.error("Test connection error:", error);
    return NextResponse.json(
      { error: "Connection failed", details: (error as Error).message },
      { status: 503 }
    );
  }
}