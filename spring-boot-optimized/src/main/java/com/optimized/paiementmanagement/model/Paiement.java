package com.optimized.paiementmanagement.model;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.springframework.data.annotation.CreatedDate;
import org.springframework.data.annotation.LastModifiedDate;
import org.springframework.data.jpa.domain.support.AuditingEntityListener;

import java.math.BigDecimal;
import java.time.LocalDateTime;

/**
 * Payment Entity - Optimized with:
 * - Proper indexing on frequently queried fields
 * - Audit fields (createdDate, modifiedDate)
 * - Builder pattern for flexible object creation
 * - Lombok annotations to reduce boilerplate
 */
@Entity
@Table(name = "paiements", indexes = {
    @Index(name = "idx_reservation_id", columnList = "reservation_id"),
    @Index(name = "idx_status", columnList = "status"),
    @Index(name = "idx_date_paiement", columnList = "date_paiement")
})
@EntityListeners(AuditingEntityListener.class)
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Paiement {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(name = "reservation_id", nullable = false)
    private Long reservationId;
    
    @Column(nullable = false, precision = 10, scale = 2)
    private BigDecimal montant;
    
    @Column(name = "date_paiement", nullable = false)
    private LocalDateTime datePaiement;
    
    @Enumerated(EnumType.STRING)
    @Column(nullable = false, length = 20)
    private PaiementStatus status;
    
    @Column(name = "mode_paiement", nullable = false, length = 50)
    private String modePaiement;
    
    @Column(name = "transaction_id", unique = true, length = 100)
    private String transactionId;
    
    @CreatedDate
    @Column(name = "created_date", nullable = false, updatable = false)
    private LocalDateTime createdDate;
    
    @LastModifiedDate
    @Column(name = "modified_date")
    private LocalDateTime modifiedDate;
    
    @Version
    private Long version; // For optimistic locking
    
    public enum PaiementStatus {
        PENDING,
        COMPLETED,
        FAILED,
        REFUNDED,
        CANCELLED
    }
}
