-- Stage 3b — supplier onboarding + suggest-a-supplier + demand ledger
-- Spec v1.1 §7, §8A, §8B.  Idempotent.  Target named per run (staging first).

CREATE TABLE IF NOT EXISTS beverage_demand_ledger (
    id                    BIGSERIAL PRIMARY KEY,
    product_id            INTEGER REFERENCES beverage_products(id) ON DELETE SET NULL,
    producer_id           INTEGER REFERENCES beverage_producers(id) ON DELETE SET NULL,
    origin_region         TEXT,
    reader_region         TEXT NOT NULL,
    reader_city           TEXT,
    event_kind            TEXT NOT NULL CHECK (event_kind IN ('view','search','suggestion')),
    search_terms          TEXT,
    local_provider_absent BOOLEAN NOT NULL DEFAULT TRUE,
    created_at            TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_demand_reader_region ON beverage_demand_ledger(reader_region);
CREATE INDEX IF NOT EXISTS idx_demand_created ON beverage_demand_ledger(created_at);

CREATE TABLE IF NOT EXISTS supplier_verification_queue (
    id                    BIGSERIAL PRIMARY KEY,
    business_name         TEXT NOT NULL,
    website               TEXT,
    claimed_regions       TEXT[],
    supplier_type         TEXT,
    source                TEXT NOT NULL CHECK (source IN ('member_suggestion','founder_assisted','inbound')),
    suggested_by_user_id  INTEGER,
    context_product_id    INTEGER,
    context_producer_id   INTEGER,
    note                  TEXT,
    status                TEXT NOT NULL DEFAULT 'suggested'
                          CHECK (status IN ('suggested','checks_running','verified_listed',
                                            'claim_pending','verified_provider','flagged','rejected')),
    check_results         JSONB DEFAULT '{}'::jsonb,
    flag_reason           TEXT,
    created_at            TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    resolved_at           TIMESTAMPTZ
);
CREATE INDEX IF NOT EXISTS idx_svq_status ON supplier_verification_queue(status);
CREATE INDEX IF NOT EXISTS idx_svq_created ON supplier_verification_queue(created_at);
