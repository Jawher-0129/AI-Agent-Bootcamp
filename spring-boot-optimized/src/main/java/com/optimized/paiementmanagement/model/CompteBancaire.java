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
 * Bank Account Entity - Optimized with:
 * - Unique constraint on account number
 * - Audit fields
 * - Optimistic locking for concurrent updates
 */
@Entity
@Table(name = "comptes_bancaires", indexes = {
    @Index(name = "idx_numero_compte", columnList = "numero_compte", unique = true)
})
@EntityListeners(AuditingEntityListener.class)
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class CompteBancaire {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(name = "numero_compte", nullable = false, unique = true, length = 34)
    private String numeroCompte;
    
    @Column(nullable = false, precision = 15, scale = 2)
    private BigDecimal solde;
    
    @Column(nullable = false, length = 100)
    private String titulaire;
    
    @Column(name = "type_compte", nullable = false, length = 20)
    private String typeCompte;
    
    @Enumerated(EnumType.STRING)
    @Column(nullable = false, length = 20)
    private CompteStatus status;
    
    @CreatedDate
    @Column(name = "created_date", nullable = false, updatable = false)
    private LocalDateTime createdDate;
    
    @LastModifiedDate
    @Column(name = "modified_date")
    private LocalDateTime modifiedDate;
    
    @Version
    private Long version;
    
    public enum CompteStatus {
        ACTIVE,
        SUSPENDED,
        CLOSED
    }
}
